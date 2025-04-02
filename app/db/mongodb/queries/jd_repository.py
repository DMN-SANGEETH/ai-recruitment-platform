from app.db.mongodb.client import MongoDBClient
from app.db.mongodb.models.job_description import JobDescription
from app.utils.logger import logger

class JobDescriptionRepository:
    def __init__(self):
        self.collection = MongoDBClient.get_instance().get_collection('job-descriptions')
        
    def create(self, job_description):
        try:
            result = self.collection.insert_one(job_description.dict())
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting job description: {e}")
        
    def find_by_id(self, id):
        result = self.collection.find_one({"_id": id})
        return JobDescription(**result) if result else None
        
    def find_all(self, limit=100, skip=0):
        cursor = self.collection.find().skip(skip).limit(limit)
        return [JobDescription(**doc) for doc in cursor]
        
    def find_by_domain(self, domain):
        cursor = self.collection.find({"domain": domain})
        return [JobDescription(**doc) for doc in cursor]
        
    def vector_search(self, embedding, limit=10):
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "job_embedding_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": limit
                }
            }
        ]
        results = self.collection.aggregate(pipeline)
        return [JobDescription(**doc) for doc in results]