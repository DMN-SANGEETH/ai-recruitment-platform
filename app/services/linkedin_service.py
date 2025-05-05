"""LinkedIn Service"""
import os
import requests
from typing import Dict, List
import google.generativeai as genai
from pydantic import HttpUrl
from app.core.llm.linkedin_processor import LinkedInProcessor
from app.core.validation.linkedin_validator import LinkedInValidation
from app.utils import logger
from app.utils.config import LinkedInConfig
from app.db.mongodb.models.linkedin import LinkedInProfile, LinkedInRequestPayload
from app.utils.exceptions import ProfileProcessingError

class LinkedInService:
    """LinkedIn Service"""
    def __init__(self):
        """Initialize the LinkedIn Service"""
        self.api_key = LinkedInConfig.get_relevance_ai_api_key()
        self.endpoint = LinkedInConfig.get_relevance_ai_endpoint()
        self.project_id = LinkedInConfig.get_relevance_ai_project_id()
        self.api_timeout = LinkedInConfig.get_relevance_ai_api_timeout()
        self.validator = LinkedInValidation
        self.linkedin_request_payload = LinkedInRequestPayload
        self.linkedin_processor = LinkedInProcessor()

    async def fetch_raw_profile(self, linkedin_url: HttpUrl) -> Dict[str, any]:
        """Fetch raw profile data from LinkedIn API"""

        validate_url = self.validator.validate_linkedin_url(linkedin_url)
        if not validate_url:
            logger.error("Invalid LinkedIn URL")
            return {
                "error": "Invalid LinkedIn URL format",
                "success": False
            }

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.api_key
            }

            payload = {
                "linkedin_url": linkedin_url,
                "return_keys": {
                    "first_name": True,
                    "last_name": True,
                    "full_name": True,
                    "headline": True,
                    "about": True,
                    "location": True,
                    "experiences": True,
                    "education": True,
                    "skills": True,
                    "profile_image_url": False
                },
                "filter_empty": True,
                "job_history_count": 3,
                "output_format": "JSON"
            }
            response = requests.post(
                f"{self.endpoint}?project={self.project_id}",
                headers=headers,
                json=payload,
                timeout=int(self.api_timeout)
            )

            # Debug response type
            response.raise_for_status()
            output = response.json().get("output", {})

            # Ensure required fields exist
            if not output.get('full_name'):
                output['full_name'] = f"{output.get('first_name', '')} {output.get('last_name', '')}".strip()

            return output

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                "error": f"API request failed: {str(e)}",
                "success": False
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "success": False
            }



    async def scraping_linkedin_content(self, linkedin_url: HttpUrl) -> LinkedInProfile:

        """Fetch and process LinkedIn profile, returning string representation"""
        try:
            raw_data = await self.fetch_raw_profile(linkedin_url)
            if not raw_data:
                raise ProfileProcessingError("No data returned from LinkedIn API")

            # Ensure raw_data is a dictionary
            if not isinstance(raw_data, dict):
                raise ProfileProcessingError("Invalid profile data format")

            # Create profile with URL
            profile_data = raw_data.copy()
            profile_data["profile_url"] = str(linkedin_url)

            profile = LinkedInProfile(**profile_data)

            # Convert profile to string representation
            profile_str = str(profile)
            print("type===================================", profile_str)
            return profile_str

        except Exception as e:
            logger.error(f"Error processing LinkedIn profile: {str(e)}")
            raise ProfileProcessingError(f"Profile processing failed: {str(e)}")

    async def process_linkedin_data(self, resume_text: str) -> Dict[str, any]:
        """Process resume file with robust error handling"""
        try:
            if not resume_text:
                logger.error("Empty text extracted from resume")
                return {
                    "error": "No text extracted",
                    "success": False
                }

            # Process resume data
            resume_data = self.linkedin_processor.process_linkedin(resume_text)
            if not resume_data:
                logger.error("Failed to process resume data")
                return {
                    "error": "Resume processing failed",
                    "success": False
                }

            return {
                "data": resume_data,
                "success": True
            }

        except Exception as e:
            logger.error(f"Unexpected error processing resume: {str(e)}", exc_info=True)
            return {
                "error": "Internal server error",
                "success": False
            }