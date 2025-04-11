# job_description.py
"""Job Description"""
from typing import List, Optional, Dict

from app.db.mongodb.models.base import MongoBaseModel

class JobDescription(MongoBaseModel):
    """Job Description class"""
    title: str
    domain: str
    description: Optional[str] = None
    technology: List[str]
    company: Optional[str] = None
    location: str
    responsibilities: List[str]
    required_skills: List[str]
    experience_level: str
    education: str
    salary_range: Dict[str, int]
    posted_date: Optional[str] = None
    application_deadline: Optional[str] = None
    apply_url: Optional[str] = None
    embedding: Optional[List[float]] = None

    class Config:
        """Config Class"""
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Machine Learning Engineer",
                "domain": "Software Engineering",
                "description": "Join our team to develop cutting-edge machine learning solutions.",
                "technology": ["Python", "TensorFlow", "PyTorch", "AWS SageMaker"],
                "company": "Example Corp",
                "location": "Remote",
                "responsibilities": ["Develop machine learning models",
                                     "Collaborate with data scientists"],
                "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow"],
                "experience_level": "3-5 years",
                "education": "Master's in Computer Science or equivalent",
                "salary_range": {"min": 80000, "max": 120000},
                "posted_date": "2025/04/01",
                "application_deadline": "2025/05/01",
                "apply_url": "https://example.com/careers/ml-engineer"
            }
        }
