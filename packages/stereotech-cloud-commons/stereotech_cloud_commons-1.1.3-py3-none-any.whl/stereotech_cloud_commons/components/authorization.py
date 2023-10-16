from __future__ import annotations
import asyncio
import base64
import uuid
import time
import datetime
import ipaddress
import re
import socket
import logging
import json
from tornado.ioloop import PeriodicCallback
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
from tornado.escape import json_decode
from typing import (
    TYPE_CHECKING,
    Any,
    Tuple,
    Set,
    Optional,
    Union,
    Dict,
    List,
)

# API Key Based Authorization
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license
# Annotation imports
if TYPE_CHECKING:
    from ..confighelper import ConfigHelper
    from ..websockets import WebRequest
    from tornado.httputil import HTTPServerRequest
    from tornado.web import RequestHandler
    from . import mongo_database
    DBComp = mongo_database.MongoDatabase
    IPAddr = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    IPNetwork = Union[ipaddress.IPv4Network, ipaddress.IPv6Network]

# Helpers for base64url encoding and decoding


def base64url_encode(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def base64url_decode(data: str) -> bytes:
    pad_cnt = len(data) % 4
    if pad_cnt:
        data += "=" * (4 - pad_cnt)
    return base64.urlsafe_b64decode(data)


ONESHOT_TIMEOUT = 5
TRUSTED_CONNECTION_TIMEOUT = 3600
PRUNE_CHECK_TIME = 300 * 1000

HASH_ITER = 100000
API_USER = "_API_KEY_USER_"
TRUSTED_USER = "_TRUSTED_USER_"
RESERVED_USERS = [API_USER, TRUSTED_USER]
JWT_EXP_TIME = datetime.timedelta(hours=1)
JWT_HEADER = {
    'alg': "EdDSA",
    'typ': "JWT"
}


class Authorization:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()
        self.auth_server = config.get('auth_server', None)
        if self.auth_server is None:
            raise config.error("auth_server is required")
        self.force_logins = config.getboolean('force_logins', False)
        self.trusted_users: Dict[IPAddr, Any] = {}
        self.permitted_paths: Set[str] = set()

        # Get allowed cors domains
        self.cors_domains: List[str] = []
        cors_cfg = config.get('cors_domains', "").strip()
        cds = [d.strip() for d in cors_cfg.split('\n') if d.strip()]
        for domain in cds:
            bad_match = re.search(r"^.+\.[^:]*\*", domain)
            if bad_match is not None:
                raise config.error(
                    f"Unsafe CORS Domain '{domain}'.  Wildcards are not"
                    " permitted in the top level domain.")
            if domain.endswith("/"):
                self.server.add_warning(
                    f"Invalid domain '{domain}' in option 'cors_domains',  "
                    "section [authorization].  Domain's cannot contain a "
                    "trailing slash.")
            else:
                self.cors_domains.append(
                    domain.replace(".", "\\.").replace("*", ".*"))

        # Get Trusted Clients
        self.trusted_ips: List[IPAddr] = []
        self.trusted_ranges: List[IPNetwork] = []
        self.trusted_domains: List[str] = []
        tcs = config.get('trusted_clients', "")
        trusted_clients = [c.strip() for c in tcs.split('\n') if c.strip()]
        for val in trusted_clients:
            # Check IP address
            try:
                tc = ipaddress.ip_address(val)
            except ValueError:
                pass
            else:
                self.trusted_ips.append(tc)
                continue
            # Check ip network
            try:
                tc = ipaddress.ip_network(val)
            except ValueError:
                pass
            else:
                self.trusted_ranges.append(tc)
                continue
            # Check hostname
            self.trusted_domains.append(val.lower())

        t_clients = "\n".join(
            [str(ip) for ip in self.trusted_ips] +
            [str(rng) for rng in self.trusted_ranges] +
            self.trusted_domains)
        c_domains = "\n".join(self.cors_domains)

        logging.info(
            f"Authorization Configuration Loaded\n"
            f"Trusted Clients:\n{t_clients}\n"
            f"CORS Domains:\n{c_domains}")

        self.prune_handler = PeriodicCallback(
            self._prune_conn_handler, PRUNE_CHECK_TIME)
        self.prune_handler.start()

        pps = config.get('permitted_paths', "")
        permitted_paths = [c.strip() for c in pps.split('\n') if c.strip()]
        for val in permitted_paths:
            self.permitted_paths.add(val)

    async def _auth_server_request(self, endpoint: str, body: Dict[str, Any] = {}, method: str = "GET"):
        try:
            http_client = AsyncHTTPClient()
            request = HTTPRequest(f"{self.auth_server}{endpoint}", method, {"Content-Type": "application/json"},
                                  json.dumps(body))
            fut = http_client.fetch(request)
            resp: HTTPResponse
            resp = await asyncio.wait_for(fut, 190.)
            data = json_decode(resp.body)
            return data
        except Exception as e:
            logging.warning(e)
            return None

    def _prune_conn_handler(self) -> None:
        cur_time = time.time()
        for ip, user_info in list(self.trusted_users.items()):
            exp_time: float = user_info['expires_at']
            if cur_time >= exp_time:
                self.trusted_users.pop(ip, None)
                logging.info(
                    f"Trusted Connection Expired, IP: {ip}")

    def _check_authorized_ip(self, ip: IPAddr) -> bool:
        if ip in self.trusted_ips:
            return True
        for rng in self.trusted_ranges:
            if ip in rng:
                return True
        fqdn = socket.getfqdn(str(ip)).lower()
        if fqdn in self.trusted_domains:
            return True
        return False

    def _check_trusted_connection(self,
                                  ip: Optional[IPAddr]
                                  ) -> Optional[Dict[str, Any]]:
        if ip is not None:
            curtime = time.time()
            exp_time = curtime + TRUSTED_CONNECTION_TIMEOUT
            if ip in self.trusted_users:
                self.trusted_users[ip]['expires_at'] = exp_time
                return self.trusted_users[ip]
            elif self._check_authorized_ip(ip):
                logging.info(
                    f"Trusted Connection Detected, IP: {ip}")
                self.trusted_users[ip] = {
                    'username': TRUSTED_USER,
                    'password': None,
                    'created_on': curtime,
                    'expires_at': exp_time
                }
                return self.trusted_users[ip]
        return None

    async def check_authorized(self,
                               request: HTTPServerRequest
                               ) -> Optional[Dict[str, Any]]:
        if request.path in self.permitted_paths or \
                request.method == "OPTIONS":
            return None

        # TODO: remote auth server request
        auth_token: Optional[str] = request.headers.get("Authorization")
        if auth_token is None:
            auth_token = request.headers.get("X-Access-Token")
        if auth_token and auth_token.startswith("Bearer "):
            auth_token = auth_token[7:]
        else:
            qtoken = request.query_arguments.get('access_token', None)
            if qtoken is not None:
                auth_token = qtoken[-1].decode()
        if auth_token:
            response = await self._auth_server_request('/access/check', {
                "auth_token": auth_token
            }, 'POST')
            if response is not None:
                return response['result']
        try:
            ip = ipaddress.ip_address(request.remote_ip)
        except ValueError:
            logging.exception(
                f"Unable to Create IP Address {request.remote_ip}")
            ip = None

        ost: Optional[List[bytes]] = request.arguments.get('token', None)
        if ost is not None and ip is not None:
            response = await self._auth_server_request('/access/check', {
                "remote_ip": request.remote_ip,
                "oneshot_token": ost[-1].decode()
            }, "POST")
            if response is not None:
                return response['result']

        # Check API Key Header
        #TODO: make remote request
        # key: Optional[str] = request.headers.get("X-Api-Key")
        # if key and key == self.api_key:
        #     return self.users[API_USER]

        # If the force_logins option is enabled and at least one
        # user is created this is an unauthorized request
        if self.force_logins:
            raise HTTPError(401, "Unauthorized")

        # Check if IP is trusted
        trusted_user = self._check_trusted_connection(ip)
        if trusted_user is not None:
            return trusted_user

        raise HTTPError(401, "Unauthorized")

    def check_cors(self,
                   origin: Optional[str],
                   req_hdlr: Optional[RequestHandler] = None
                   ) -> bool:
        if origin is None or not self.cors_domains:
            return False
        for regex in self.cors_domains:
            match = re.match(regex, origin)
            if match is not None:
                if match.group() == origin:
                    logging.debug(f"CORS Pattern Matched, origin: {origin} "
                                  f" | pattern: {regex}")
                    self._set_cors_headers(origin, req_hdlr)
                    return True
                else:
                    logging.debug(f"Partial Cors Match: {match.group()}")
        else:
            # Check to see if the origin contains an IP that matches a
            # current trusted connection
            match = re.search(r"^https?://([^/:]+)", origin)
            if match is not None:
                ip = match.group(1)
                try:
                    ipaddr = ipaddress.ip_address(ip)
                except ValueError:
                    pass
                else:
                    if self._check_authorized_ip(ipaddr):
                        logging.debug(
                            f"Cors request matched trusted IP: {ip}")
                        self._set_cors_headers(origin, req_hdlr)
                        return True
            logging.debug(f"No CORS match for origin: {origin}\n"
                          f"Patterns: {self.cors_domains}")
        return False

    def _set_cors_headers(self,
                          origin: str,
                          req_hdlr: Optional[RequestHandler]
                          ) -> None:
        if req_hdlr is None:
            return
        req_hdlr.set_header("Access-Control-Allow-Origin", origin)
        if req_hdlr.request.method == "OPTIONS":
            req_hdlr.set_header(
                "Access-Control-Allow-Methods",
                "GET, POST, PUT, DELETE, OPTIONS")
            req_hdlr.set_header(
                "Access-Control-Allow-Headers",
                "Origin, Accept, Content-Type, X-Requested-With, "
                "X-CRSF-Token, Authorization, X-Access-Token, "
                "X-Api-Key")

    def close(self) -> None:
        self.prune_handler.stop()


def load_component(config: ConfigHelper) -> Authorization:
    return Authorization(config)
