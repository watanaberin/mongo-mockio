import json
from mockio.utils.myclient import mclient
        
class Op(object):
    def __init__(self, template, db_uri, num):
        self._template = template
        self._client = mclient(db_uri)
        self._num = num
    @property
    def template(self):
        return self._template

    @property
    def client(self):
        return self._client

    @property
    def num(self):
        return self._num