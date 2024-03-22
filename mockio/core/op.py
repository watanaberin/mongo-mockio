from mockio.core.client import MongoDBclient
from typing import Union, Any

class Op(object):
    def __init__(self,
                 template: dict,
                 mongodb_uri: Union[str, None],
                 db_name: Union[str, None],
                 num: Union[int, None]) -> None:
        self._template = template
        self._client = MongoDBclient(mongodb_uri, db_name)
        self._num = num if num else 100
        
    @property
    def template(self):
        return self._template

    @property
    def client(self):
        return self._client

    @property
    def num(self):
        return self._num