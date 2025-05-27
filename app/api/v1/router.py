
from fastapi import APIRouter
from app.api.v1.endpoints import linkedin, resume, profile

router = APIRouter()
router.include_router(resume.router, prefix="/resumes", tags=["resumes"])
router.include_router(linkedin.router, prefix="/linkedin", tags=["linkedin"])
router.include_router(profile.router, prefix="/profile", tags=["profile"])

