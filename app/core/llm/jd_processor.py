from typing import List, Dict, Any
from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.core.rag.embeddings import EmbeddingGenerator
from app.utils.logger import logger


class JobDescriptionProcessor:
    def __init__(self):
        """Initialize the Job Description Processor"""
        self.repository = JobDescriptionRepository()
        self.embedding = EmbeddingGenerator()

    def _transform_job_data(self, raw_data: Dict[str, Any], domain: str):
        """Transform raw job description data into standardized format"""
        return {
            "title": raw_data.get("job_title", raw_data.get("title", "")),
            "domain": domain,
            "description": raw_data.get("job_description",raw_data.get("description", "")),
            "company": raw_data.get("job_company",raw_data.get("company", "")),
            "technology": raw_data.get("technology_requirement", raw_data.get("technology", [])),
            "location": raw_data.get("location", ""),
            "responsibilities": raw_data.get("key_responsibilities", raw_data.get("responsibilities", [])),
            "required_skills": raw_data.get("required_skills", []),
            "experience_level": raw_data.get("experience_level_requirement",
                                           raw_data.get("experience_level", "")),
            "education": raw_data.get("education_requirement", raw_data.get("education", "")),
            "salary_range": raw_data.get("salary_range", {"min": 0, "max": 0}),
            "posted_date": raw_data.get("posted_date",""),
            "application_deadline": raw_data.get("application_deadline", ""),
            "apply_url": raw_data.get("apply_url",""),
        }

    def process_job_descriptions(self, domain: str, job_descriptions: List[Dict[str, Any]]):
        """Process and store job descriptions for a domain"""
        if not job_descriptions or not isinstance(job_descriptions, list):
            logger.error(f"No valid job descriptions provided for domain: {domain}")
            return 0

        successful_count = 0

        for jd_data in job_descriptions:
            try:
                transformed_data = self._transform_job_data(jd_data, domain)

                embedding = self.embedding.create_job_description_embedding(transformed_data)
                transformed_data["embedding"] = embedding

                jd = JobDescription(**transformed_data)
                #Create db
                result = self.repository.create(jd)

                if result:
                    successful_count += 1
                    logger.debug(f"Stored job description: {transformed_data['title']}")
                else:
                    logger.warning(f"Failed to store job description: {transformed_data['title']}")

            except Exception as e:
                logger.error(f"Error processing job description: {str(e)}")
                continue
        return successful_count