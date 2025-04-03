# app/db/mongo/queries/base_crud.py
from typing import TypeVar, Generic, Type, List, Dict, Any, Optional
from app.db.mongodb.client import MongoDBClient
from app.db.mongodb.models.base import MongoBaseModel
from bson import ObjectId
from datetime import datetime
from app.utils.logger import logger

T = TypeVar('T', bound=MongoBaseModel)

class BaseCrudRepository(Generic[T]):
    def __init__(self, model_class: Type[T], collection_name: str):
        self.model_class = model_class
        self.collection = MongoDBClient.get_instance().get_collection(collection_name)
        
    def create(self, model: T) -> str:
        """Create a new document."""
        try:
            model_dict = model.model_dump(by_alias=True)  # Changed from dict()
            result = self.collection.insert_one(model_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
        
        
    def find_by_id(self, id: str) -> Optional[T]:
        """Find a document by ID."""
        try:
            result = self.collection.find_one({"_id": ObjectId(id)})
            return self.model_class(**result) if result else None
        except Exception as e:
            logger.error(f"Error find_by_id job description: {e}")
        
    def update(self, id: str, update_data: Dict[str, Any]) -> bool:
        """Update a document."""
        try:
            update_data["updated_at"] = datetime.now()
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
                    logger.error(f"Error Update job description: {e}")
        
    def delete(self, id: str) -> bool:
        """Delete a document."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
                logger.error(f"Error delete job description: {e}")
        
    def find_many(self, query: Dict[str, Any], limit: int = 100, skip: int = 0) -> List[T]:
        """Find documents matching query."""
        try:
            cursor = self.collection.find(query).skip(skip).limit(limit)
            return [self.model_class(**doc) for doc in cursor]
        except Exception as e:
                logger.error(f"Error find_all job description: {e}")