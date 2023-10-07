

import json
import logging
from ..confighelper import ConfigHelper
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Union,
    List
)

class NotificationService:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()
        self.notification_url = config.get('notification_url')
        self.client = AsyncHTTPClient()

    async def send_email(self, to: str, subject: str = 'Stereotech Cloud', content: str = '') -> Any:
        request = HTTPRequest(self.notification_url + '/server/email/send','POST',{
            'Content-Type': 'application/json'
        }, body=json.dumps({
            'destination_address': to,
            'subject': subject,
            'email_message': content
        }))
        try:
            result = await self.client.fetch(request)
            return json.loads(result.body)
        except Exception as e:
            logging.info("Error sending email: %s" % e)
            return None

def load_component(config: ConfigHelper) -> NotificationService:
    return NotificationService(config)