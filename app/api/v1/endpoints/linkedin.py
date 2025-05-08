# app/api/routes/resume_upload.py (for example)

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List
import requests

from pydantic import HttpUrl

from app.db.mongodb.models.job_filter import LinkedInProfileResponse
from app.services.job_service import JobService
from app.services.linkedin_service import LinkedInService

from app.services.resume_service import ResumeService
from app.utils import logger


router = APIRouter()

linkedin_service = LinkedInService()
resume_service = ResumeService()
job_service = JobService()

def validate_linkedin_url(url):
    """Validate LinkedIn URL format"""
    valid_prefixes = (
        "https://www.linkedin.com/in/",
        "http://www.linkedin.com/in/",
        "https://linkedin.com/in/",
        "http://linkedin.com/in/"
    )
    return any(url.startswith(prefix) for prefix in valid_prefixes)



@router.post("/upload/url", response_model=LinkedInProfileResponse, status_code=status.HTTP_201_CREATED)
async def upload_linkedin_profile(linkedin_url: HttpUrl):
    """Handle LinkedIn profile upload and return string representation"""
    try:
        url_str = str(linkedin_url)
        if not validate_linkedin_url(url_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid LinkedIn URL format"
            )
        
        profile_data = await linkedin_service.scraping_linkedin_content(linkedin_url=url_str)
        
        return profile_data
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions as they're already formatted correctly
        logger.error(f"HTTP error while processing LinkedIn profile: {str(http_ex)}")
        raise
    except ValueError as val_err:
        # Handle validation errors from validator or other sources
        logger.error(f"Validation error: {str(val_err)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error processing LinkedIn profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the LinkedIn profile"
        )