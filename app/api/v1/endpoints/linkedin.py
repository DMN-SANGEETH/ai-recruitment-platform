# app/api/routes/resume_upload.py (for example)

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List

from pydantic import HttpUrl

from app.db.mongodb.models.job_match import JobMatchResponse
from app.services.job_service import JobService
from app.services.linkedin_service import LinkedInService

from app.services.resume_service import ResumeService
from app.utils import logger


router = APIRouter()

linkedin_service = LinkedInService()
resume_service = ResumeService()
job_service = JobService()




# @router.post("/upload", response_model=List[JobMatchResponse], status_code=status.HTTP_201_CREATED)
# async def upload_linkedin_profile(linkedin_url: HttpUrl):
#     """Handle resume file upload and return job matches"""
#     try:
#         profile_data = await linkedin_service.scraping_linkedin_content(
#             linkedin_url=str(linkedin_url)
#         )
#         print("type===================================",type(profile_data))
#         return profile_data

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error processing resume: {str(e)}", exc_info=True)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error processing resume: {str(e)}"
#         )

# app/api/routes/linkedin.py

@router.post("/upload", response_model=List[JobMatchResponse], status_code=status.HTTP_201_CREATED)
async def upload_linkedin_profile(linkedin_url: HttpUrl):
    """Handle LinkedIn profile upload and return string representation"""
    try:
        print("linkedin_url",linkedin_url)
        profile_data = await linkedin_service.scraping_linkedin_content(
            linkedin_url=str(linkedin_url))
        print("profile_data===================================", profile_data)

        resume_data = await linkedin_service.process_linkedin_data(profile_data)

        if not resume_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process resume"
            )

        results = job_service.get_job_matches_for_resume(resume_data)
        if not results:
            raise HTTPException(status_code=404, detail="No matching jobs found")

        response = [
            {
                "title": job["job"]["title"],
                "company": job["job"].get("company"),
                "domain": job["job"]["domain"],
                "match_percentage": float(job["match_percentage"]),
                "explanation": job["explanation"],
                "salary_range": job["job"]["salary_range"],
                "location": job["job"]["location"],
                "apply_url": job["job"].get("apply_url")
            }
            for job in results
        ]

        return response
                # return JSONResponse(
        #     content=jsonable_encoder({
        #         "status": "success",
        #         "original_filename": uploaded_file.filename,
        #         "data": results
        #     }),
        #     status_code=status.HTTP_201_CREATED
        # )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )