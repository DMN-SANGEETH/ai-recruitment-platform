from pymongo import MongoClient
from pymongo.errors import PyMongoError
from app.utils.logger import logger

class TestDatabase:
    """Handles database testing operations"""

    def __init__(self,
                 client: MongoClient,
                 test_db_name: str = "test_db"
                 ):
        self.client = client
        self.test_db = self.client[test_db_name]
        self.test_collection = self.test_db["test_collection"]

    def test_connection(self) -> bool:
        """Test basic database connection"""
        try:
            self.client.admin.command('ping')
            logger.info("Database connection test passed")
            return True
        except PyMongoError as e:
            logger.error(f"Connection test failed: {str(e)}")
            raise

    def test_basic_operations(self) -> bool:
        """Test CRUD operations"""
        try:
            # Test insert
            doc = {"test": "value", "number": 42}
            insert_result = self.test_collection.insert_one(doc)
            assert insert_result.inserted_id is not None

            # Test read
            found = self.test_collection.find_one({"_id": insert_result.inserted_id})
            assert found["test"] == "value"

            # Test update
            update_result = self.test_collection.update_one(
                {"_id": insert_result.inserted_id},
                {"$set": {"number": 100}}
            )
            assert update_result.modified_count == 1

            # Test delete
            delete_result = self.test_collection.delete_one({"_id": insert_result.inserted_id})
            assert delete_result.deleted_count == 1

            logger.info("All database operations test passed")
            return True
        except PyMongoError as e:
            logger.error(f"Database operations test failed: {str(e)}")
            raise
        finally:
            # Cleanup
            self.test_db.drop_collection("test_collection")