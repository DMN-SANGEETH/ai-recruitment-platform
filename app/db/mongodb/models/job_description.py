# job_description.py
from typing import List, Optional, Dict
from pydantic import Field

from app.db.mongodb.models.base import MongoBaseModel

class JobDescription(MongoBaseModel):
    title: str
    domain: str
    technology:List[str]
    company: Optional[str] = None
    location: str
    responsibilities: List[str]
    required_skills: List[str]
    experience_level: str
    education: str
    salary_range: Dict[str, int]
    embedding: Optional[List[float]] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Machine Learning Engineer",
                "domain": "Software Engineering",
                "technology_requirement": ["Experience with cloud-based machine learning platforms (e.g., AWS SageMaker, Azure Machine Learning)"],
                "company": "Example Corp",
                "location": "Remote",
                "responsibilities": ["Develop web applications", "Collaborate with team"],
                "required_skills": ["JavaScript", "Python", "React", "Node.js"],
                "experience_level": "3-5 years",
                "education": "Bachelor's in Computer Science or equivalent",
                "salary_range": {"min": 80000, "max": 120000}
            }
        }