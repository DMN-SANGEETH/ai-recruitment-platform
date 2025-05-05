
from typing import Any

from fastapi import APIRouter
from app.api.v1.endpoints import linkedin, resume



router = APIRouter()
router.include_router(resume.router, prefix="/resumes", tags=["resumes"])
router.include_router(linkedin.router, prefix="/linkedin", tags=["linkedin"])

