from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from typing import Union
class MongoDBclient:
    URI = 'mongodb://localhost:27017'
    DB = 'test'
    def __init__(self, uri: str, db: str) -> None:
        uri = uri if uri else self.URI
        db = db if db else self.DB
        self.client = MongoClient(uri, serverSelectionTimeoutMS=1000)
        self.db = self.client[db]
                
    def bulk_insert(self, col, datas):
        self.db[col].insert_many(datas)
    
    def is_connect(self) -> bool:
        try:
            self.client.server_info()
        except ServerSelectionTimeoutError:
            return False
        return True
    
    def is_writable(self) -> bool:
        return self.client.is_primary
