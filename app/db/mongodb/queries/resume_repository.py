"""Resume Repository"""

from typing import List

from app.db.mongodb.queries.base_crud import BaseCrudRepository
from app.db.mongodb.models.resume import Resume
from app.utils.logger import logger


class ResumeRepository(BaseCrudRepository[Resume]):
    """Resume  Repository class"""
    def __init__(self):
        super().__init__(Resume, "job-resumes")

    def find_by_domain(self,
                       domain
                       ) -> List[Resume]:
        """Find resumes by domain."""
        try:
            cursor = self.collection.find({"domain": domain})
            return [Resume(**doc) for doc in cursor]
        except Exception as e:
            logger.error("Error in find_by_domain: %s", e)  # Lazy % formatting
            raise  # Re-raise the exception after logging (recommended)

    def find_by_skills(self,
                       skills: List[str],
                       limit: int = 10
                       ) -> List[Resume]:
        """Find CVs that require any of the given skills."""
        try:
            return self.find_many({"required_skills": {"$in": skills}}, limit)
        except Exception as e:
            logger.error("Error in find_by_skills: %s", e)  # Fixed method name in log
            raise

    def vector_search(self,
                      embedding: List[float],
                      limit: int = 10
                      ) -> List[dict]:
        """Find CV by vector similarity."""
        try:
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
            results = self.collection.aggregate(pipeline)

            return [{"job": Resume(**doc["document"]), "score": doc["score"]}
                    for doc in results]
        except Exception as e:
            logger.error("Error in vector search for resumes: %s", e)
            raise
