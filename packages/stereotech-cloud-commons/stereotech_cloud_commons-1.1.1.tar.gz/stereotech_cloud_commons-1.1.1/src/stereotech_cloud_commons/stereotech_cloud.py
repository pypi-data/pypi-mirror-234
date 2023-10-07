#!/usr/bin/env python3
# StereotechCloud - HTTP/Websocket API Server for Klipper
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license

from __future__ import annotations
import argparse
from asyncio.events import new_event_loop
import sys
import importlib
import os
import io
import time
import socket
import logging
import json
import signal
from . import confighelper
import asyncio
from tornado import iostream
from tornado.netutil import Resolver
from .eventloop import EventLoop
from .app import StereotechCloud
from .utils import ServerError, SentinelClass, StereotechCloudLoggingHandler

# Annotation imports
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Callable,
    Coroutine,
    Tuple,
    Dict,
    List,
    Union,
    TypeVar,
)
if TYPE_CHECKING:
    from .websockets import WebRequest, Subscribable
    FlexCallback = Callable[..., Optional[Coroutine]]
    _T = TypeVar("_T")

INIT_TIME = .25
LOG_ATTEMPT_INTERVAL = int(2. / INIT_TIME + .5)
MAX_LOG_ATTEMPTS = 10 * LOG_ATTEMPT_INTERVAL

CORE_COMPONENTS = [
    'mongo_database', "authorization", "notification", "storage"]

SENTINEL = SentinelClass.get_instance()


class Server:
    error = ServerError

    def __init__(self,
                 args: Dict[str, Any],
                 file_logger: Optional[StereotechCloudLoggingHandler],
                 event_loop: EventLoop
                 ) -> None:
        self.event_loop = event_loop
        self.file_logger = file_logger
        self.app_args = args
        self.config = config = confighelper.get_configuration(self, args)  # type: ignore
        # log config file
        strio = io.StringIO()
        config.write_config(strio)
        cfg_item = f"\n{'#'*20} StereotechCloud Configuration {'#'*20}\n\n"
        cfg_item += strio.getvalue()
        cfg_item += "#"*65
        strio.close()
        self.add_log_rollover_item('config', cfg_item)
        self.host: str = config.get('host', "0.0.0.0")
        self.port: int = config.getint('port', 7125)
        self.domain: str = config.get('domain', self.host)
        self.ssl_port: int = config.getint('ssl_port', 7130)
        self.exit_reason: str = ""

        # Event initialization
        self.events: Dict[str, List[FlexCallback]] = {}

        # Tornado Application/Server
        self.server_running: bool = False
        self.stereotech_cloud_app = app = StereotechCloud(config)
        self.register_endpoint = app.register_local_handler
        self.register_static_file_handler = app.register_static_file_handler
        self.get_websocket_manager = app.get_websocket_manager
        self.register_api_transport = app.register_api_transport
        self.register_notification_transport = app.register_notification_transport
        self.register_notification = app.register_notification

        self.failed_components: List[str] = []
        self.warnings: List[str] = []

        self.register_endpoint(
            "/server/info", ['GET'], self._handle_info_request)
        #self.register_endpoint(
        #    "/server/config", ['GET'], self._handle_config_request)
        #self.register_endpoint(
        #    "/server/restart", ['POST'], self._handle_server_restart)

        self.register_notification(
            'server:websocket_removed', transports=[])


        # Component initialization
        self.components: Dict[str, Any] = {}
        self._load_components(config)
        config.validate_config()

    def get_app_args(self) -> Dict[str, Any]:
        return dict(self.app_args)

    def get_event_loop(self) -> EventLoop:
        return self.event_loop

    def start(self) -> None:
        hostname, hostport = self.get_host_info()
        logging.info(
            f"Starting StereotechCloud on ({self.host}, {hostport}), "
            f"Hostname: {hostname}")
        self.stereotech_cloud_app.listen(self.host, self.port, self.ssl_port)
        self.server_running = True
        self.event_loop.add_signal_handler(
            signal.SIGTERM, self._handle_term_signal)

    def add_log_rollover_item(self, name: str, item: str,
                              log: bool = True) -> None:
        if self.file_logger is not None:
            self.file_logger.set_rollover_info(name, item)
        if log and item is not None:
            logging.info(item)

    def add_warning(self, warning: str, log: bool = True) -> None:
        if log:
            logging.warning(warning)

    # ***** Component Management *****
    def _load_components(self, config: confighelper.ConfigHelper) -> None:
        # load core components
        for component in CORE_COMPONENTS:
            self.load_component(config, component, __package__)

        # check for optional components
        opt_sections = set([s.split()[0] for s in config.sections()])
        opt_sections.remove('server')
        for section in opt_sections:
            self.load_component(config, section, None)

    def load_component(self,
                       config: confighelper.ConfigHelper,
                       component_name: str,
                       package: Optional[str] = None,
                       default: Union[SentinelClass, _T] = SENTINEL
                       ) -> Union[_T, Any]:
        if component_name in self.components:
            return self.components[component_name]
        try:
            path = ".components." if package is not None else "components."
            module = importlib.import_module(path + component_name, package)
            func_name = "load_component"
            if hasattr(module, "load_component_multi"):
                func_name = "load_component_multi"
            if component_name not in CORE_COMPONENTS and \
                    func_name == "load_component":
                config = config[component_name]
            load_func = getattr(module, func_name)
            component = load_func(config)
        except Exception:
            msg = f"Unable to load component: ({component_name})"
            logging.exception(msg)
            self.failed_components.append(component_name)
            if isinstance(default, SentinelClass):
                raise ServerError(msg)
            return default
        self.components[component_name] = component
        logging.info(f"Component ({component_name}) loaded")
        return component

    def lookup_component(self,
                         component_name: str,
                         default: Union[SentinelClass, _T] = SENTINEL
                         ) -> Union[_T, Any]:
        component = self.components.get(component_name, default)
        if isinstance(component, SentinelClass):
            raise ServerError(f"Component ({component_name}) not found")
        return component

    def set_failed_component(self, component_name: str) -> None:
        if component_name not in self.failed_components:
            self.failed_components.append(component_name)

    def register_event_handler(self,
                               event: str,
                               callback: FlexCallback
                               ) -> None:
        self.events.setdefault(event, []).append(callback)

    def send_event(self, event: str, *args) -> None:
        events = self.events.get(event, [])
        for evt in events:
            self.event_loop.register_callback(evt, *args)

    def get_host_info(self) -> Tuple[str, int]:
        hostname = socket.gethostname()
        return hostname, self.port

    def _handle_term_signal(self) -> None:
        logging.info(f"Exiting with signal SIGTERM")
        self.event_loop.register_callback(self._stop_server, "terminate")

    async def _stop_server(self, exit_reason: str = "restart") -> None:
        self.server_running = False
        # Call each component's "on_exit" method
        for name, component in self.components.items():
            if hasattr(component, "on_exit"):
                func: FlexCallback = getattr(component, "on_exit")
                try:
                    ret = func()
                    if ret is not None:
                        await ret
                except Exception:
                    logging.exception(
                        f"Error executing 'on_exit()' for component: {name}")

        # Sleep for 100ms to allow connected websockets to write out
        # remaining data
        await asyncio.sleep(.1)
        try:
            await self.stereotech_cloud_app.close()
        except Exception:
            logging.exception("Error Closing App")

        # Close all components
        for name, component in self.components.items():
            if hasattr(component, "close"):
                func = getattr(component, "close")
                try:
                    ret = func()
                    if ret is not None:
                        await ret
                except Exception:
                    logging.exception(
                        f"Error executing 'close()' for component: {name}")

        self.exit_reason = exit_reason
        self.event_loop.remove_signal_handler(signal.SIGTERM)
        self.event_loop.stop()

    async def _handle_server_restart(self, web_request: WebRequest) -> str:
        self.event_loop.register_callback(self._stop_server)
        return "ok"

    async def _handle_info_request(self,
                                   web_request: WebRequest
                                   ) -> Dict[str, Any]:

        resolver = Resolver()
        hostname, hostport = self.get_host_info()
        address = await resolver.resolve(hostname, hostport)
        methods = []
        for key, definition in self.stereotech_cloud_app.api_cache.items():
            methods.extend(definition.jrpc_methods)
        return {
            #'address': address,
            'components': list(self.components.keys()),
            'failed_components': self.failed_components,
            'plugins': list(self.components.keys()),
            'failed_plugins': self.failed_components,
            'warnings': self.warnings,
            'methods': methods
        }

    async def _handle_config_request(self,
                                     web_request: WebRequest
                                     ) -> Dict[str, Any]:
        return {
            'config': self.config.get_parsed_config()
        }

# Basic WebRequest class, easily converted to dict for json encoding


class BaseRequest:
    def __init__(self, rpc_method: str, params: Dict[str, Any]) -> None:
        self.id = id(self)
        self.rpc_method = rpc_method
        self.params = params
        self._event = asyncio.Event()
        self.response: Any = None

    async def wait(self) -> Any:
        # Log pending requests every 60 seconds
        start_time = time.time()
        while True:
            try:
                await asyncio.wait_for(self._event.wait(), 60.)
            except asyncio.TimeoutError:
                pending_time = time.time() - start_time
                logging.info(
                    f"Request '{self.rpc_method}' pending: "
                    f"{pending_time:.2f} seconds")
                self._event.clear()
                continue
            break
        if isinstance(self.response, ServerError):
            raise self.response
        return self.response

    def notify(self, response: Any) -> None:
        self.response = response
        self._event.set()

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'method': self.rpc_method,
                'params': self.params}
