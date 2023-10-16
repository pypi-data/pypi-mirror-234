import json
import logging
from typing import Any, Callable, List, Optional, Dict
from ..confighelper import ConfigHelper
from ..eventloop import EventLoop
from .mongo_database import JSONEncoder
import pika
from pika import adapters
from pika.adapters.tornado_connection import TornadoConnection
from pika.exchange_type import ExchangeType
from pika.channel import Channel
from pika.spec import Basic, BasicProperties


class PublisherConsumer:
    def __init__(self, ampq_url: str, exchange: str, queue: str, routing_keys: List[str], on_message_cb: Callable, loop: EventLoop) -> None:
        # Connection specific
        self._connection = Optional[TornadoConnection]
        self._loop = loop
        self._channel = Optional[Channel]
        self._consumer_tag = None

        self._closing = False
        self._url = ampq_url
        self._exchange = exchange
        self._consume_queue = queue
        self._routing_keys = routing_keys

        self._on_message_cb = on_message_cb

    def connect(self):
        logging.info('Connecting to %s', self._url)
        self._connection = TornadoConnection(
            pika.URLParameters(self._url), self._on_connection_open)

    def _on_connection_open(self, unused_connection: pika.SelectConnection):
        logging.info('Connection opened')
        logging.info('Adding connection close callback')
        self._connection.add_on_close_callback(self._on_connection_closed)
        logging.info('Creating a new channel')
        self._connection.channel(on_open_callback=self._on_channel_open)

    def _on_connection_closed(self, connection: TornadoConnection, reason: Exception):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            logging.warning('Connection closed, reopening in 5 seconds: %s',
                            reason)
            self._connection.ioloop.call_later(5, self._reconnect)

    def _reconnect(self):
        if not self._closing:
            # Create a new connection
            self._connection = self.connect()

    def _on_channel_open(self, channel: Channel):
        logging.info('Channel opened')
        self._channel = channel
        logging.info('Adding channel close callback')
        self._channel.add_on_close_callback(self._on_channel_closed)
        self._setup_exchange(self._exchange)

    def _on_channel_closed(self, channel, reason):
        logging.warning('Channel %i was closed: %s', channel, reason)
        self._connection.close()

    def _setup_exchange(self, exchange_name: str):
        logging.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(
            callback=self._on_exchange_declareok,
            durable=True,
            exchange=exchange_name,
            exchange_type=ExchangeType.topic,
        )

    def _on_exchange_declareok(self, unused_frame):
        logging.info('Exchange declared')
        self._setup_queue(self._consume_queue)

    def _setup_queue(self, queue_name: str):
        logging.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(
            queue=queue_name,
            durable=True,
            callback=self._on_queue_declareok,
        )

    def _on_queue_declareok(self, method_frame):
        logging.info('Binding %s to %s with %s',
                     self._exchange, self._consume_queue, self._routing_keys)
        for routing_key in self._routing_keys:
            self._channel.queue_bind(
                queue=self._consume_queue,
                exchange=self._exchange,
                routing_key=routing_key,
                callback=self._start_consuming,
            )

    def _start_consuming(self, method_frame):
        logging.info('Issuing consumer related RPC commands')
        logging.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self._on_consumer_cancelled)
        self._consumer_tag = self._channel.basic_consume(
            on_message_callback=self._on_message,
            queue=self._consume_queue,
        )

    def _on_consumer_cancelled(self, method_frame):
        logging.info('Consumer was cancelled remotely, shutting down: %r',
                     method_frame)
        if self._channel:
            self._channel.close()

    def _on_message(self, unused_channel: Channel, basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
        logging.info('Received message # %s from %s: %s',
                     basic_deliver.delivery_tag, properties.app_id, body)
        self._channel.basic_ack(basic_deliver.delivery_tag)
        self._on_message_cb(
            {'routing_key': basic_deliver.routing_key, 'payload': json.loads(body)})

    def publish_message(self, routing_key: str, message: Any, headers: Optional[Dict[str, str]] = None):
        if self._channel is None or not self._channel.is_open:
            return
        properties = pika.BasicProperties(app_id=self._consume_queue,
                                          content_type='application/json',
                                          headers=headers)
        self._channel.basic_publish(self._exchange, routing_key,
                                    json.dumps(
                                        message, ensure_ascii=False, cls=JSONEncoder),
                                    properties)


class MqService:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()
        self.amqp_url = config.get('ampq_url', None)
        if self.amqp_url is None:
            return
        self.amqp_exchange = config.get('ampq_exchange', 'notify')
        self.amqp_consume_queue = config.get(
            'amqp_consume_queue', 'common')  # Must have equal name as service
        self.amqp_consume_keys = [c.strip()
                                  for c in config.get('amqp_consume_keys', '').split('\n') if c.strip()]

        self.server.register_notification('mq:message_received', transports=[])
        notification_cache = self.server.register_notification_transport(
            'mq', self)
        for evt_name, notification in notification_cache.items():
            if "mq" in notification.supported_transports:
                self.register_notification(evt_name, notification.notify_name)

        self.pub_con = PublisherConsumer(self.amqp_url, self.amqp_exchange, self.amqp_consume_queue,
                                         self.amqp_consume_keys, self.on_message, self.server.get_event_loop())
        self.server.get_event_loop().delay_callback(1.0, self.pub_con.connect)

    def on_message(self, message: Any):
        self.server.send_event('mq:message_received', message)

    def register_notification(self,
                              event_name: str,
                              notify_name: Optional[str] = None
                              ) -> None:
        if notify_name is None:
            notify_name = event_name
        notify_name = notify_name.replace(':', '.')

        def notify_handler(*args):
            self.pub_con.publish_message(notify_name, *args)

        self.server.register_event_handler(
            event_name, notify_handler)


def load_component(config: ConfigHelper) -> MqService:
    return MqService(config)
