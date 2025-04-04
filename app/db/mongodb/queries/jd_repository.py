from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.base_crud import BaseCrudRepository
from app.utils.logger import logger
from typing import Dict, List, Optional

class JobDescriptionRepository(BaseCrudRepository[JobDescription]):
    def __init__(self):
        super().__init__(JobDescription, "job-descriptions")

    def find_by_domain(self, domain):
        """Fined by domain"""
        try:
            cursor = self.collection.find({"domain": domain})
            return [JobDescription(**doc) for doc in cursor]
        except Exception as e:
            logger.error(f"Error find_by_domain job description: {e}")
    

    def find_by_skills(self, skills: List[str], limit: int = 10) -> List[JobDescription]:
        """Find job descriptions that require any of the given skills."""
        try:
            return self.find_many({"required_skills": {"$in": skills}}, limit)
        except Exception as e:
                logger.error(f"Error find_by_domain job description: {e}")
    
    def get_all_with_embeddings(self) -> List[Dict]:
        """Get all job descriptions that have embeddings"""
        return list(self.collection.find(
            {"embedding": {"$exists": True, "$ne": None}},
            {"embedding": 1, "title": 1, "required_skills": 1, "domain": 1}  # Include other fields you need
        ))
    
        
    def vector_search(self, embedding: List[float], limit: int = 10):
        """Find job descriptions by vector similarity."""
        try:
            print(f"Querying with embedding (first 5 dims): {embedding[:5]}")
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "job_descriptions_embedding_vector_index",
                        "path": "embedding",
                        "queryVector": embedding,
                        "numCandidates": 100,
                        "limit": limit
                    }
                },
                    {
                        "$project": {
                            "document": "$$ROOT",
                            "score": {"$meta": "vectorSearchScore"}
                        }
                    }
                ]
            results = list(self.collection.aggregate(pipeline))
            print("============================================")
            print(f"Found {len(results)} matches")
            print("results:",results)
            
            return [{"job": JobDescription(**doc["document"]), "score": doc["score"]} 
                    for doc in results]
        except Exception as e:
            logger.error(f"Error in vector search for JD: {e}")
            raise