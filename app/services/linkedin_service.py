"""LinkedIn Service"""

from datetime import time
from fastapi import HTTPException
import requests
from typing import Any, Dict

from pydantic import HttpUrl
from fastapi import HTTPException, status
from app.core.llm.linkedin_processor import LinkedInProcessor
from app.core.validation.linkedin_validator import LinkedInValidation
from app.utils import logger
from app.utils.config import LinkedInConfig
from app.utils.exceptions import LinkedInAPIError, ProfileProcessingError

class LinkedInService:
    """LinkedIn Service"""
    def __init__(self):
        """Initialize the LinkedIn Service"""
        self.api_key = LinkedInConfig.get_relevance_ai_api_key()
        self.endpoint = LinkedInConfig.get_relevance_ai_endpoint()
        self.project_id = LinkedInConfig.get_relevance_ai_project_id()
        self.api_timeout = LinkedInConfig.get_relevance_ai_api_timeout()
        self.validator = LinkedInValidation

        self.linkedin_processor = LinkedInProcessor()

    async def scraping_linkedin_content(self, linkedin_url: str) -> Dict:
        """Fetch and process LinkedIn profile, returning structured data"""

        headers = self._prepare_request_headers()
        payload = self._prepare_request_payload(linkedin_url)


        print("payload=========",payload)
        print("type_payload=========",type(payload))
        print("=======================",f"{self.endpoint}?project={self.project_id}")
        try:
            response = self._make_api_request(headers,payload)
            profile_data = self._process_api_response(response)
            # Record request duration for monitoring

            return profile_data


        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error accessing LinkedIn API: {str(conn_err)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not connect to LinkedIn API service"
            )
            
        except LinkedInAPIError as api_err:
            logger.error(f"LinkedIn API error: {str(api_err)}")
            raise HTTPException(
                status_code=api_err.status_code,
                detail=api_err.detail
            )
            
        except Exception as e:
            logger.error(f"Unexpected error in LinkedIn service: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
            
    def _prepare_request_headers(self) -> Dict[str, str]:
        """Prepare API request headers"""
        return {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        
    def _prepare_request_payload(self, linkedin_url: str) -> Dict[str, Any]:
        """Prepare API request payload with all required fields"""
        return {
            "linkedin_url": linkedin_url,
            "return_keys": {
                "first_name": True,
                "last_name": True,
                "full_name": True,
                "profile_id": True,
                "headline": True,
                "about": True,
                "job_title": True,
                "location": True,
                "city": True,
                "country": True,
                "profile_image_url": False,
                "public_id": True,
                "urn": True,
                "linkedin_url": True,
                "company": True,
                "company_domain": True,
                "company_employee_range": True,
                "company_industry": True,
                "company_linkedin_url": True,
                "company_website": True,
                "company_year_founded": True,
                "hq_city": True,
                "hq_country": True,
                "current_company_join_month": True,
                "current_company_join_year": True,
                "current_job_duration": True,
                "experiences": True
            },
            "filter_empty": True,
            "job_history_count": 10,
            "output_format": "JSON"
        }
        
    def _make_api_request(self, headers: Dict[str, str], payload: Dict[str, Any]) -> requests.Response:
        """Make API request with error handling"""
        try:
            response = requests.post(
                f"{self.endpoint}?project={self.project_id}",
                headers=headers,
                json=payload,
                timeout=int(self.api_timeout)
            )
            
            # Check for HTTP errors
            if response.status_code != 200:
                logger.error(f"LinkedIn API returned non-200 status: {response.status_code}")
                raise LinkedInAPIError(
                    status_code=response.status_code,
                    detail=f"LinkedIn API request failed with status {response.status_code}: {response.text}"
                )
                
            return response
        
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.api_timeout}s")
            raise
            
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error: {str(req_err)}")
            raise LinkedInAPIError(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"API request failed: {str(req_err)}"
            )
            
    def _process_api_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process API response and extract profile data"""
        try:
            response_data = response.json()
            
            # Check if output exists
            if response_data.get("output") is None:
                logger.error("Empty output from LinkedIn API")
                raise LinkedInAPIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No data returned from LinkedIn API"
                )
            
            # Extract output data
            output_data = response_data["output"]
            
            # Normalize company data
            if isinstance(output_data.get("company"), str):
                output_data["company"] = {"name": output_data["company"]}
            
            return output_data
            
        except ValueError as json_err:
            logger.error(f"Invalid JSON response: {str(json_err)}")
            raise LinkedInAPIError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid response from LinkedIn API"
            )
    
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