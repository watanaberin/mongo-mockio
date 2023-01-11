from pymongo import MongoClient

class MyClient:
    def __init__(self, host, db) -> None:
        self.client = MongoClient(host)
        self.db = self.client[db]
    
    def bulk_insert(self, col, datas):
        self.db[col].insert_many(datas)