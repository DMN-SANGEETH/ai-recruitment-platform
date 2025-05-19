"""Resume Linkedin processor"""
import json
from typing import  Any, Dict, Tuple
from fastapi import HTTPException, status
import google.generativeai as genai
import requests

from app.core.llm.gemini_client import GeminiClient
from app.core.llm.linkedin_processor import LinkedInProcessor
from app.core.llm.prompt_template import RESUME_LINKEDIN_PROCESSOR_TEMPLATE, RESUME_PROCESSOR_TEMPLATE, RESUME_VALIDATION_TEMPLATE
from app.core.validation.linkedin_validator import LinkedInValidation
from app.db.mongodb.models.resume import Resume, Education, Experience
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.core.rag.embeddings import EmbeddingGenerator
from app.services.linkedin_service import LinkedInService
from app.utils.exceptions import LinkedInAPIError
from app.utils.logger import logger
from app.utils.config import LinkedInConfig, MongoDBConfig
from app.utils.helpers import extract_and_validate_json

class ResumeLinkedinProcessor:
    """Resume Processor class"""
    def __init__(self):
        """Initialize the Resume Processor with Gemini"""
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        self.model = genai.GenerativeModel("gemini-1.5-flash") #gemini-1.5-flash gemini-1.5-pro
        self.repository = ResumeRepository()
        self.embedding = EmbeddingGenerator()
        self.linkedin_service = LinkedInService()
        self.validate_linkedin = LinkedInValidation()
        
        self.api_key = LinkedInConfig.get_relevance_ai_api_key()
        self.endpoint = LinkedInConfig.get_relevance_ai_endpoint()
        self.project_id = LinkedInConfig.get_relevance_ai_project_id()
        self.api_timeout = LinkedInConfig.get_relevance_ai_api_timeout()
        self.validator = LinkedInValidation

        self.linkedin_processor = LinkedInProcessor()

        self.gemini_client = GeminiClient(
            model=self.model,
            initial_delay=5,
            max_retries=3,
            backoff_factor=2
        )

    def _generate_prompt(self,
                         resume_text: str
                         ):
        """Generate prompt for extracting structured information from resume text"""
        return RESUME_PROCESSOR_TEMPLATE.format(
            resume_text=resume_text
        )

    def _generate_prompt_for_linkedin(self,
                         resume_text: str,
                         linkedin_profile
                         ):
        """Generate prompt for extracting structured information from resume text"""
        return RESUME_LINKEDIN_PROCESSOR_TEMPLATE.format(resume_text=resume_text, linkedin_profile=linkedin_profile)

    def _generate_validation_prompt(self,
                                    text: str
                                    ):
        """Generate prompt to validate if the text is a resume"""
        return RESUME_VALIDATION_TEMPLATE.format(
            text=text
        )

    def validate_resume(self,
                        text: str
                        ) -> Tuple[bool, str]:
        """
        Check if the provided text is a valid resume
        """
        if not text or len(text.strip()) < 100:
            return False, "Text is too short to be a valid resume"

        try:
            prompt = self._generate_validation_prompt(text)
            response = self.gemini_client._call_gemini_with_retry(prompt,
                                                                  domain="resume_validation"
                                                                  )

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
            logger.error("Error validating resume: %s", str(e))
            return False, f"Validation error: {str(e)}"

    def _transform_resume_data(self,
                               data: str,
                               file_path: str = None
                               ):
        """Transform extracted JSON data into standardized resume format"""
        try:
            resume_data = {
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "linkedin_url": data.get("linkedin_url", ""),
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
            logger.error("Error transforming resume data: %s", str(e))
            return {}


    async def _linkedin_scraping(self,
                           json_content,
                           ):
        linkedin_url = json_content.get("linkedin_url")
        print("linkedin_url=========== 66", linkedin_url)  # Should print: https://www.linkedin.com/in/dmn-sangeeth
        print("linkedin_url type=========== 66", type(linkedin_url))
        # Proceed with scraping
        if linkedin_url:
            print(type(linkedin_url))
            url_str = str(linkedin_url)
            print(type(url_str))
            if not self.validate_linkedin.validate_linkedin_url_pr(url_str):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid LinkedIn URL format"
                )
            headers = self._prepare_request_headers()
            payload = self._prepare_request_payload(linkedin_url)

            response = self._make_api_request(headers,payload)
            profile_data = self._process_api_response(response)

            #linkedin_profile = await self.linkedin_service.scraping_linkedin_content(linkedin_url = url_str)
            # print("linkedin_profile=========== 7", profile_data)
            # print("linkedin_profile type=========== 7", type(profile_data))
            return profile_data
        else:
            logger.error("No LinkedIn URL found in resume data")

    async def process_resume_linkedin(self,
                       resume_text: str,
                       file_path: str = None
                       ):
        """Process resume text to extract structured information and store in database"""
        if not resume_text:
            logger.error("No resume text provided")
            return None

        try:
            # First validate if this is a resume
            is_valid, validation_reason = self.validate_resume(resume_text)

            if not is_valid:
                logger.warning("Invalid resume detected: %s", validation_reason)
                return {
                    "is_valid_resume": False,
                    "validation_reason": validation_reason
                }
            # print("resume_text 18 =========================", resume_text)
            prompt = self._generate_prompt(resume_text)
            # print("content: 3 =========",prompt)
            content = self.gemini_client._call_gemini_with_retry(prompt,
                                                                 domain="resume_processing"
                                                                 )
            # print("prompt: 3 =========",content)
            if not content:
                logger.error("Failed to extract information from resume")
                return None

            cleaned_resume_content = extract_and_validate_json(content)
            if not cleaned_resume_content:
                logger.error("Invalid JSON content extracted from resume")
                return None
            print("cleaned_linkedin_content: 4 =========",cleaned_resume_content)
            print("cleaned_linkedin_content: 4 type=========",type(cleaned_resume_content))
            json_content = json.loads(cleaned_resume_content) if isinstance(cleaned_resume_content, str) else cleaned_resume_content

            resume_data = self._transform_resume_data(json_content, file_path)
            #print("resume_data 12==========================", type(resume_data))
            #print("resume_data 12==========================", resume_data)
            
            # if json_content.get("linkedin_url"):
            #     try:
            #         linkedin_profile = await self._linkedin_scraping(json_content)
            #         if linkedin_profile:
            #             # Optionally save the LinkedIn profile JSON to a file
            #             with open('linkedin_profile.json', 'w') as f:
            #                 json.dump(linkedin_profile, f)
            #         else:
            #             logger.warning("Failed to get LinkedIn profile data")
            #         if not linkedin_profile:
            #             logger.warning("Failed to get LinkedIn profile data")
            #     except Exception as e:
            #         logger.error(f"Error scraping LinkedIn: {str(e)}")
            #         # Continue with just resume data if LinkedIn fails

            # If we have LinkedIn data, merge it

            try:
                with open('linkedin_profile.json', 'r') as f:
                    linkedin_profile = json.load(f)
                    #print("merge_data 10==========================", type(merge_data_content))
                    #print(type(linkedin_profile))
                    #print("linkedin_profile:===========",linkedin_profile)
            except FileNotFoundError:
                logger.info("No saved LinkedIn profile found")
            # print("resume_text===========",resume_text)
            merge_prompt = self._generate_prompt_for_linkedin(resume_text, linkedin_profile)
            #print("merge_prompt==============", merge_prompt)
            merge_data_content = self.gemini_client._call_gemini_with_retry(
                merge_prompt, domain="resume_linkedin_processing"
            )
            #print("merge_data_content",merge_data_content)
            if merge_data_content:
                cleaned_merge_content = extract_and_validate_json(merge_data_content)
                if cleaned_merge_content:
                    merged_data = json.loads(cleaned_merge_content) if isinstance(cleaned_merge_content, str) else cleaned_merge_content
                    # Update resume_data with merged content
                    resume_data.update(merged_data)
                    
            print("merge_data 10==========================", type(merge_data_content))
            print("merge_data 10==========================", merge_data_content)
            print("cv data 11==================================", type(resume_data))
            print("cv data 11==================================", resume_data)
            
            #prompt_linkedin = self._generate_prompt(linkedin_profile)
            #print("content: 4 =========",prompt_linkedin)
            #linkedin_content = self.gemini_client._call_gemini_with_retry(prompt_linkedin,
                                                                #  domain="linkedin_processing"
                                                                #  )
            
            #cleaned_linkedin_content = extract_and_validate_json(linkedin_content)
            # if not cleaned_linkedin_content:
            #     logger.error("Invalid JSON content extracted from resume")
            #     return None
            #print("cleaned_linkedin_content: 4 =========",cleaned_linkedin_content)
            #print("cleaned_linkedin_content: 4 type=========",type(cleaned_linkedin_content))
            # json_linkedin_content = json.loads(cleaned_linkedin_content) if isinstance(cleaned_linkedin_content, str) else cleaned_linkedin_content
            
            # linkedin_data = self._transform_linkedin_data(json_linkedin_content)
           # print("linkedin_data 12==========================", type(linkedin_data))
            #print("linkedin_data 12==========================", linkedin_data)
            
            try:
                embedding = self.embedding.create_resume_embedding(resume_data)
                resume_data["embedding"] = embedding

                # Process education and experience
                education_list = []
                for edu in resume_data.get("education", []):
                    education_list.append(Education(**edu))
                resume_data["education"] = education_list

                experience_list = []
                for exp in resume_data.get("experience", []):
                    experience_list.append(Experience(**exp))
                resume_data["experience"] = experience_list

                resume = Resume(**resume_data)

                # Store in DB if valid
                if is_valid:
                    result = self.repository.create(resume)
                    if not result:
                        logger.error("Failed to store resume for %s", resume_data.get("name", "unknown"))

                return {
                    "resume_data": resume_data,
                    "success": True,
                    "is_valid_resume": is_valid
                }

            except Exception as e:
                logger.error(f"Error finalizing resume data: {str(e)}")
                return {
                    "error": f"Error finalizing resume data: {str(e)}",
                    "success": False,
                    "partial_data": resume_data
                }

        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return {
                "error": f"Error processing resume: {str(e)}",
                "success": False
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

    def _prepare_request_headers(self) -> Dict[str, str]:
        """Prepare API request headers"""
        return {
            "Content-Type": "application/json",
            "Authorization": self.api_key
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