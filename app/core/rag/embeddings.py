"""Embedding Generation"""
from typing import List, Dict, Any, Tuple
import google.generativeai as genai

from app.utils.logger import logger
from app.utils.config import MongoDBConfig


class EmbeddingGenerator:
    """Embedding Generation Class"""
    def __init__(self):
        """Initialize the embedding generate with gemini API"""
        try:
            genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
            self.model = genai.embed_content
            logger.info("Embedding generator initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize embedding generator: %s", e)
            raise

    def generate_embedding(self,
                           text:str
                           ) -> Tuple[List[float], int]:
        """Generate Embedding for given text using gemini model"""
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            embedding = result["embedding"]
            logger.debug("Successfully generated embedding of dimension %d",
                         len(embedding)
                         )
            return embedding

        except Exception as e:
            logger.error("Error generating embedding: %s", e)
            raise

    def create_job_description_embedding(self,
                                         job_data: Dict[str, Any]
                                         ) -> List[float]:
        """Create embedding for job description by combing relevant field"""
        try:
            combined_text = f"""
            Job Title: {job_data.get("title", '')}
            Domain: {job_data.get("domain", '')}
            Technologies: {', '.join(job_data.get('technology', []))}
            Location: {job_data.get('location', '')}
            Responsibilities: {' '.join(job_data.get('responsibilities', []))}
            Required Skills: {', '.join(job_data.get('required_skills', []))}
            Experience Level: {job_data.get('experience_level', '')}
            Education: {job_data.get('education', '')}
            Salary Range: {job_data.get('salary_range', '')}
            Posted Date: {job_data.get('posted_date', '')}
            Salary Range: {job_data.get('salary_range', '')}
            Application Deadline: {job_data.get('application_deadline', '')}
            Apply Url: {job_data.get('apply_url', '')}
            """
            embedding = self.generate_embedding(combined_text)
            logger.info("Successfully created embedding for job: %s", job_data.get("title"))
            return embedding

        except Exception as e:
            logger.error("Failed to create job description embedding: %s",e)
            return []

    def create_resume_embedding(self,
                                resume_data: Dict[str, Any]
                                ) -> List[float]:
        """Create embedding for resume by combining relevant fields"""
        try:
            skills_str = ', '.join(resume_data.get('skills', []))

            experience_str = ""
            for exp in resume_data.get('experience', []):

                if isinstance(exp, dict):
                    title = exp.get('title', '')
                    company = exp.get('company', '')
                    description = exp.get('description', '')

                    experience_str += f"{title} at {company}. {description} "

            education_str = ""
            for edu in resume_data.get('education', []):
                if isinstance(edu, dict):
                    degree = edu.get('degree', '')
                    institution = edu.get('institution', '')

                    education_str += f"{degree} from {institution}. "

            combined_text = f"""
            Name: {resume_data.get('name', '')}
            Summary: {resume_data.get('summary', '')}
            Skills: {skills_str}
            Experience: {experience_str}
            Education: {education_str}
            Certifications: {', '.join(resume_data.get('certifications', []))}
            """

            embedding = self.generate_embedding(combined_text)
            logger.info("Successfully created embedding for resume: %s",
                        resume_data.get("name")
                        )
            return embedding

        except Exception as e:
            logger.error("Failed to create resume embedding: %s", e)
            return []
        