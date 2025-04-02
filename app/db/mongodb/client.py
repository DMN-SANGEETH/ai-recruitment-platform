from pymongo import MongoClient
from app.utils.config import MongoDBConfig

class MongoDBClient:
    _instance = None 

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if MongoDBClient._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MongoDBClient._instance = self
            self.client = MongoClient(MongoDBConfig.get_mongodb_uri())
            self.db = self.client.recruitment_platform
            
    def get_collection(self, collection_name):
        return self.db[collection_name]