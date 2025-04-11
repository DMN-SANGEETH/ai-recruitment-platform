"""Mongo DB Client"""
from pymongo import MongoClient

from app.utils.config import MongoDBConfig

class MongoDBClient:
    """Mongo DB Client Class"""
    _instance = None

    @classmethod
    def get_instance(cls):
        """Instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initial method"""
        if MongoDBClient._instance is not None:
            raise RuntimeError("This class is a singleton!")
        else:
            MongoDBClient._instance = self
            self.client = MongoClient(MongoDBConfig.get_mongodb_uri())
            self.db = self.client.recruitment_platform

    def get_collection(self,
                       collection_name
                       ):
        """Get collection"""
        return self.db[collection_name]
