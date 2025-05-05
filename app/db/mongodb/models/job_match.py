# app/api/schemas/job_match.py

from pydantic import BaseModel
from typing import List, Optional, Dict


class SalaryRange(BaseModel):
    min: int
    max: int


class JobMatchResponse(BaseModel):
    title: str
    company: Optional[str] = None
    domain: str
    match_percentage: float
    explanation: str
    salary_range: SalaryRange
    location: str
    apply_url: Optional[str] = None
