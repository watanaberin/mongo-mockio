import json
from mockio.utils.myclient import mclient
from typing import Union, Any
class Op(object):
    def __init__(self, template: Any, db_uri: Union[str, None], num: Union[int, None]):
        self._template = template
        self._client = mclient(db_uri if db_uri else "localhost:27017/test")
        self._num = num if num else 1
        
    @property
    def template(self):
        return self._template

    @property
    def client(self):
        return self._client

    @property
    def num(self):
        return self._num