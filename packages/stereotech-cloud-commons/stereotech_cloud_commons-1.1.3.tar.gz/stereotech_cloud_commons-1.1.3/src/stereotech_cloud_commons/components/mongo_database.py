from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Union
from urllib.parse import quote_plus as quote

from bson import ObjectId, json_util
from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor
from pymongo.mongo_client import MongoClient

from ..utils import SentinelClass

if TYPE_CHECKING:
    from pymongo.mongo_client import MongoClient

    from ..confighelper import ConfigHelper
    from ..websockets import WebRequest

PRINTJOB_NAMESPACE = "printjobs"

SENTINEL = SentinelClass.get_instance()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, Cursor):
            return list(o)
        if isinstance(o, CommandCursor):
            return list(o)
        return json.JSONEncoder.default(self, o)

class JSONDecoder(json.JSONDecoder):
    def decode(self, s: str):
        s = s.replace("\"_id\":", "\"id\":")
        return json.JSONDecoder.decode(self, s)

def parse_json(data):
    return json.loads(JSONEncoder().encode(data), cls=JSONDecoder)

class MongoDatabase:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()
        self.database_path = config.get(
            'database_path', 'localhost'
        )
        self.database_port: int = config.getint(
            'database_port', 49153
        )
        self.database_name = config.get(
            'database_name', 'stereotech_cloud'
        )
        self.user = config.get(
            'user_name', ''
        )
        self.pw = config.get(
            'password', ''
        )
        self.rs = config.get(
            'rs', ''
        )
        self.auth_src = config.get(
            'auth_src', ''
        )
        self.tlsCAFile = config.get(
            'tlscafile', ''
        )

        url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
            user=quote(self.user),
            pw=quote(self.pw),
            hosts=','.join([
                '{path}:{port}'.format(path=self.database_path, port=self.database_port)
            ]),
            rs=self.rs,
            auth_src=self.auth_src)
        self.client: MongoClient[Dict[str, Any]] = MongoClient(
            url,
            tlsCAFile=self.tlsCAFile)
        self.db = self.client[self.database_name]


        #self.server.register_endpoint(
        #    "/server/database/list", ['GET'], self._handle_list_request)
        #self.server.register_endpoint(
        #    "/server/database/item", ["GET", "POST", "DELETE"],
        #    self._handle_item_request)

    def __getitem__(self, name):
        return self.db[name]

    async def _handle_item_request(self, web_request: WebRequest) -> \
            Dict[str, Any]:
        action = web_request.get_action()
        collection = web_request.get_str("collection")
        if action == 'GET':
            id = web_request.get_str("id")
            item = self.get_item(collection, id)
            str_item = parse_json(item)
            return {"item": str_item}
        if action == 'DELETE':
            id = web_request.get_str("id")
            self.delete_item(collection, id)
            str_id = parse_json(id)
            return {'deleted_jobs': [str_id]}
        if action == 'POST':
            id = web_request.get_str("id", None)
            value = web_request.get("value")
            obj = json.loads(value)
            if id is None:
                # insert_item
                self.insert_item(collection, obj)
            else:
                # update_item
                self.update_item(collection, id, obj)
            return {"item": {}}
        raise self.server.error("Invalid Request Method")

    async def _handle_list_request(self, web_request: WebRequest) -> Dict[str, Any]:
        collection = web_request.get_str("collection")
        value = self.db[collection].find()
        list_val = list(parse_json(value))
        return {"value": list_val}

    def insert_item(self,
                    collection: str,
                    value: Union[List[Any], Any]) -> List[Any]:
        db_collection = self.db[collection]
        normalized_value: List[Any] = []
        if type(value) is not List:
            normalized_value = [value]
        else:
            normalized_value = value
        result = db_collection.insert_many(normalized_value)
        return result.inserted_ids

    def update_item(self,
                    collection: str,
                    key: str,
                    value: Any):
        db_collection = self.db[collection]
        result = db_collection.update_one({'_id': ObjectId(key)}, {'$set': value})
        return result.upserted_id

    def delete_item(self,
                    collection: str,
                    key: str):
        db_collection = self.db[collection]
        result = db_collection.delete_many({'_id': ObjectId(key)})
        return result.deleted_count

    def get_item(self,
                 collection: str,
                 key: str,
                 default: Any = SENTINEL) -> Any:
        db_collection = self.db[collection]
        result = db_collection.find_one({"_id": ObjectId(key)})
        if result is None:
            return default
        return result

def load_component(config: ConfigHelper) -> MongoDatabase:
    return MongoDatabase(config)
