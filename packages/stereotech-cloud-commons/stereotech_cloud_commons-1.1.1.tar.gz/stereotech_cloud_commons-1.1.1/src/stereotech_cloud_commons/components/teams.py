from __future__ import annotations
import asyncio
import logging
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse
from tornado.escape import json_decode
from tornado.httputil import url_concat
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

if TYPE_CHECKING:
    from ..confighelper import ConfigHelper
    from ..websockets import WebRequest
    from tornado.httputil import HTTPServerRequest
    from tornado.web import RequestHandler


class Teams:
    def __init__(self, config: ConfigHelper) -> None:
        """
        The service allows to get information about the current user team
        """
        self.server = config.get_server()
        self.teams_server = config.get("teams_server", None)
        if self.teams_server is None:
            raise config.error("teams_server is required")

    async def check_team(self, request: HTTPServerRequest
                               ) -> Optional[Dict[str, Any]]:
        try:
            endpoint: str = "/server/teams/team",
            url = url_concat(f"{self.teams_server}{endpoint}", request.arguments)
            http_client = AsyncHTTPClient()
            request = HTTPRequest(
                url, "GET", headers=request.headers
            )
            fut = http_client.fetch(request)
            resp: HTTPResponse
            resp = await asyncio.wait_for(fut, 190.0)
            data = json_decode(resp.body)
            return data
        except Exception as e:
            logging.warning(e)
            return None



def load_component(config: ConfigHelper) -> Teams:
    return Teams(config)
