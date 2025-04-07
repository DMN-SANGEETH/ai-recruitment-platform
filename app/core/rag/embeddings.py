from app.utils.logger import logger
import google.generativeai as genai
from app.utils.config import MongoDBConfig
from typing import List, Dict, Any, Optional

class EmbeddingGenerator:
    def __init__(self):
        """Initialize the embedding generate with gemini API"""
        try:
            genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
            self.model = genai.embed_content
            logger.info("Embedding generator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize embedding generator: {e}")
            raise

    def generate_embedding(self, text:str) -> List[float]:
        """Generate Embedding for given text using gemini model"""
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            embedding = result["embedding"]
            logger.debug(f"Successfully generated embedding of dimension {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def create_job_description_embedding(self, job_data: Dict[str, Any]) -> List[float]:
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
            """
            embedding = self.generate_embedding(combined_text)
            logger.info(f"Successfully created embedding for job: {job_data.get('title')}")
            return embedding
        except Exception as e:
             logger.error(f"Failed to create job description embedding: {e}")
             return []

    def create_resume_embedding(self, resume_data: Dict[str, Any]) -> List[float]:
        """Create embedding for resume by combining relevant fields"""
        try:
            skills_str = ', '.join(resume_data.get('skills', []))

            experience_str = ""
            for exp in resume_data.get('experience', []):
                if isinstance(exp, dict):
                    experience_str += f"{exp.get('title', '')} at {exp.get('company', '')}. {exp.get('description', '')} "

            education_str = ""
            for edu in resume_data.get('education', []):
                if isinstance(edu, dict):
                    education_str += f"{edu.get('degree', '')} from {edu.get('institution', '')}. "

            combined_text = f"""
            Name: {resume_data.get('name', '')}
            Summary: {resume_data.get('summary', '')}
            Skills: {skills_str}
            Experience: {experience_str}
            Education: {education_str}
            Certifications: {', '.join(resume_data.get('certifications', []))}
            """

            embedding = self.generate_embedding(combined_text)
            logger.info(f"Successfully created embedding for resume: {resume_data.get('name')}")
            return embedding
        except Exception as e:
             logger.error(f"Failed to create resume embedding: {e}")
             return []