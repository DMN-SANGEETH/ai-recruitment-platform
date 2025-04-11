"""JD Processor"""
from typing import List, Dict, Any

from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.core.rag.embeddings import EmbeddingGenerator
from app.utils.logger import logger
from app.utils.exceptions import StoreJobDescription, GetCountOfFailures


class JobDescriptionProcessor:
    """Job Description Processor class"""
    def __init__(self):
        """Initialize the Job Description Processor"""
        try:
            self.repository = JobDescriptionRepository()
            self.embedding = EmbeddingGenerator()
            logger.info("JobDescriptionProcessor initialized successfully")
        except Exception as e:
            logger.critical("Failed to initialize JobDescriptionProcessor: %s", e, exc_info=True)
            raise

    def _generate_embedding(self,
                            job_data: Dict[str, Any]
                            ) -> List[float]:
        """Generate embedding with proper error handling."""
        try:
            embedding = self.embedding.create_job_description_embedding(job_data)
            if not embedding or not isinstance(embedding, list):
                raise ValueError("Invalid embedding generated")
            return embedding
        except Exception as e:
            logger.error("Embedding generation failed for job '%s': %s",
                       job_data.get("title"), e, exc_info=True)
            raise

    def _store_job_description(self,
                               job_data: Dict[list, any]
                               ) -> bool:
        """Store job description with transaction safety."""
        try:
            jd = JobDescription(**job_data)
                #Create db
            result = self.repository.create(jd)

            if not result:
                raise ValueError("Database operation returned False")
            return True

        except StoreJobDescription as e:
            logger.error("Failed to store job '%s': %s",
                       job_data.get("title"), e, exc_info=True)
            return False

    def _transform_job_data(self,
                            raw_data: Dict[str, Any],
                            domain: str
                            ):
        """Transform raw job description data into standardized format"""

        try:
            transformed = {
                "title": raw_data.get("job_title", raw_data.get("title", "")),
                "domain": domain,
                "description": raw_data.get("job_description",
                                            raw_data.get("description", "")),
                "company": raw_data.get("job_company",raw_data.get("company", "")),
                "technology": raw_data.get("technology_requirement",
                                        raw_data.get("technology", [])),
                "location": raw_data.get("location", ""),
                "responsibilities": raw_data.get("key_responsibilities",
                                                raw_data.get("responsibilities", [])),
                "required_skills": raw_data.get("required_skills", []),
                "experience_level": raw_data.get("experience_level_requirement",
                                            raw_data.get("experience_level", "")),
                "education": raw_data.get("education_requirement",
                                        raw_data.get("education", "")),
                "salary_range": raw_data.get("salary_range", {"min": 0, "max": 0}),
                "posted_date": raw_data.get("posted_date",""),
                "application_deadline": raw_data.get("application_deadline", ""),
                "apply_url": raw_data.get("apply_url",""),
            }

            if not transformed["description"]:
                raise ValueError("Job description cannot be empty")

            return transformed

        except Exception as e:
            logger.error("Transformation failed for job data: %s", e, exc_info=True)
            raise

    def process_job_descriptions(self,
                                 domain: str,
                                 job_descriptions: List[Dict[str, Any]]
                                 ):
        """Process and store job descriptions for a domain"""

        if not job_descriptions or not isinstance(job_descriptions, list):
            logger.error("No valid job descriptions provided for domain: %s", domain)
            raise TypeError("Job descriptions must be a list")

        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string")

        results = {
            "total": len(job_descriptions),
            "success": 0,
            "failures": 0,
            "errors": []
        }

        for idx, jd_data in enumerate(job_descriptions):
            try:
                if not isinstance(jd_data, dict):
                    raise TypeError(f"Job description at index {idx} is not a dictionary")

                transformed_data = self._transform_job_data(jd_data, domain)

                transformed_data["embedding"] = self._generate_embedding(transformed_data)

                # Store in database
                if self._store_job_description(transformed_data):
                    results["success"] += 1
                    logger.info("Processed job: %s", transformed_data["title"])
                else:
                    raise RuntimeError("Storage failed without exception")

            except GetCountOfFailures as e:
                results["failures"] += 1
                error_info = {
                    "index": idx,
                    "error": str(e),
                    "job_title": jd_data.get("title") or jd_data.get("job_title") or f"Unknown (index {idx})"
                    }
                results["errors"].append(error_info)
                logger.warning("Failed to process job at index %d: %s", idx, e)
                continue

        logger.info(
            "Processing complete. Success: %d, Failures: %d",
            results["success"],
            results["failures"]
        )

        return results
