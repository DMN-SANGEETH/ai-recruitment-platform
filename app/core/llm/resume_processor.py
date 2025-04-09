from typing import Dict, Any, List, Tuple
import google.generativeai as genai
import json
from google.api_core import exceptions
from app.core.llm.gemini_client import GeminiClient
from app.core.llm.prompt_template import RESUME_PROCESSOR_TEMPLATE, RESUME_VALIDATION_TEMPLATE
from app.db.mongodb.models.resume import Resume, Education, Experience
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.core.rag.embeddings import EmbeddingGenerator
from app.utils.logger import logger
from app.utils.config import MongoDBConfig
from app.utils.helpers import extract_and_validate_json

class ResumeProcessor:
    def __init__(self):
        """Initialize the Resume Processor with Gemini"""
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        self.model = genai.GenerativeModel("gemini-1.5-flash") #gemini-1.5-flash gemini-1.5-pro
        self.repository = ResumeRepository()
        self.embedding = EmbeddingGenerator()

        self.gemini_client = GeminiClient(
            model=self.model,
            initial_delay=5,
            max_retries=3,
            backoff_factor=2
        )

    def _generate_prompt(self, resume_text: str):
        """Generate prompt for extracting structured information from resume text"""
        return RESUME_PROCESSOR_TEMPLATE.format(
            resume_text=resume_text
        )
    def _generate_validation_prompt(self, text: str):
        """Generate prompt to validate if the text is a resume"""
        return RESUME_VALIDATION_TEMPLATE.format(
            text=text
        )

    def validate_resume(self, text: str) -> Tuple[bool, str]:
        """
        Check if the provided text is a valid resume
        """
        if not text or len(text.strip()) < 100:
            return False, "Text is too short to be a valid resume"

        try:
            prompt = self._generate_validation_prompt(text)
            response = self.gemini_client._call_gemini_with_retry(prompt, domain="resume_validation")

            if not response:
                return False, "Unable to validate resume content"

            # Extract JSON from response
            validation_result = extract_and_validate_json(response)

            if not validation_result:
                return False, "Invalid validation response format"

            validate_data = json.loads(validation_result) if isinstance(validation_result, str) else validation_result

            is_valid = validate_data.get("is_valid_resume", False)
            reason = validate_data.get("reason", "No reason provided")

            return is_valid, reason

        except Exception as e:
            logger.error(f"Error validating resume: {str(e)}")
            return False, f"Validation error: {str(e)}"

    def _transform_resume_data(self, json_data: str, file_path: str = None):
        """Transform extracted JSON data into standardized resume format"""
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            resume_data = {
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "phone": data.get("phone", ""),
                "summary": data.get("summary", ""),
                "skills": data.get("skills", []),
                "experience": data.get("experience", []),
                "education": data.get("education", []),
                "certifications": data.get("certifications", []),
                "projects": data.get("projects", []),
                "file_path": file_path,
                "is_valid_resume":data.get("is_valid_resume",bool)
            }

            return resume_data

        except Exception as e:
            logger.error(f"Error transforming resume data: {str(e)}")
            return {}

    def process_resume(self, resume_text: str, file_path: str = None):
        """Process resume text to extract structured information and store in database"""
        if not resume_text:
            logger.error("No resume text provided")
            return None

        try:
            # First validate if this is a resume
            is_valid, validation_reason = self.validate_resume(resume_text)

            if not is_valid:
                logger.warning(f"Invalid resume detected: {validation_reason}")
                return {
                    "is_valid_resume": False,
                    "validation_reason": validation_reason
                }

            prompt = self._generate_prompt(resume_text)
            content = self.gemini_client._call_gemini_with_retry(prompt, domain="resume_processing")

            if not content:
                logger.error("Failed to extract information from resume")
                return None

            cleaned_content = extract_and_validate_json(content)
            if not cleaned_content:
                logger.error("Invalid JSON content extracted from resume")
                return None

            resume_data = self._transform_resume_data(cleaned_content, file_path)
            embedding = self.embedding.create_resume_embedding(resume_data)
            resume_data["embedding"] = embedding

            education_list = []
            for edu in resume_data.get("education", []):
                education_list.append(Education(**edu))
            resume_data["education"] = education_list

            experience_list = []
            for exp in resume_data.get("experience", []):
                experience_list.append(Experience(**exp))

            resume_data["experience"] = experience_list
            resume = Resume(**resume_data)

            # Only store in DB if it's a valid resume
            if is_valid:
                result = self.repository.create(resume)
                if result:
                    logger.info(f"Successfully processed and stored resume for {resume_data['name']}")
                else:
                    logger.error(f"Failed to store resume for {resume_data['name']}")

            return resume_data

        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return None