# app/api/routes/resume_upload.py (for example)

from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List

from app.db.mongodb.models.job_match import JobMatchResponse
from app.services.job_service import JobService
from app.services.resume_linkedin_service import ResumeLinkedinService
from app.utils.file_handling import FileHandler
from app.utils import logger


router = APIRouter()
resume_linkedin_service = ResumeLinkedinService()
job_service = JobService()


@router.post("/upload", response_model=List[JobMatchResponse], status_code=status.HTTP_201_CREATED)
async def upload_resume(uploaded_file: UploadFile = File(...)):
    """Handle resume file upload and return job matches"""
    try:
        file_extension = uploaded_file.filename.split('.')[-1].lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.{file_extension}"

        if file_extension not in FileHandler.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed types: {', '.join(FileHandler.ALLOWED_EXTENSIONS)}"
            )

        resume_data = await resume_linkedin_service.process_resume_file(
            file=uploaded_file,
            filename=filename
        )
        print("resume_data after adding cv 001:",resume_data)

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