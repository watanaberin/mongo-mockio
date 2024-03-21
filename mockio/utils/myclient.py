from pymongo import MongoClient

class mclient:
    def __init__(self, host: str, db: str) -> None:
        self.client = MongoClient(host)
        self.db = self.client[db]
        
    def __init__(self, uri: str) -> None:
        itmes = uri.split("/")
        self.client = MongoClient(itmes[0])
        self.db = self.client[itmes[1]]
        
    def bulk_insert(self, col, datas):
        self.db[col].insert_many(datas)