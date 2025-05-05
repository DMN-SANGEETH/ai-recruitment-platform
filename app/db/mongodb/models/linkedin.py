# app/models/linkedin.py
from typing import List, Optional, Dict
from pydantic import Field, HttpUrl, EmailStr
from app.db.mongodb.models.base import MongoBaseModel

class LinkedInExperience(MongoBaseModel):
    title: str
    company: str
    duration: str
    description: Optional[str] = None
    location: Optional[str] = None
    currently_working: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "duration": "2021-Present",
                "description": "Leading a team of developers",
                "location": "San Francisco, CA",
                "currently_working": True
            }
        }

class LinkedInEducation(MongoBaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: str
    year: Optional[str] = None
    duration: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "degree": "Master of Science",
                "field_of_study": "Computer Science",
                "institution": "Stanford University",
                "year": "2018",
                "duration": "2016-2018"
            }
        }

class LinkedInProfile(MongoBaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: str
    headline: Optional[str] = None
    about: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_url: HttpUrl
    profile_image_url: Optional[HttpUrl] = None
    experiences: List[LinkedInExperience] = []
    education: List[LinkedInEducation] = []
    skills: List[str] = []
    certifications: List[str] = []
    projects: List[Dict[str, str]] = []
    languages: List[str] = []
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None

class LinkedInRequestPayload(MongoBaseModel):
    linkedin_url: HttpUrl
    return_keys: Dict[str, bool] = Field(
        default_factory=lambda: {
            "first_name": True,
            "last_name": True,
            "full_name": True,
            "headline": True,
            "about": True,
            "location": True,
            "experiences": True,
            "education": True,
            "skills": True,
            "profile_image_url": False
        }
    )
    filter_empty: bool = True
    job_history_count: int = Field(default=2, gt=0, le=10)
    output_format: str = "JSON"

    class Config:
        exclude_fields = {'_id', 'created_at', 'updated_at'}
        json_encoders = {
            HttpUrl: lambda v: str(v) if v else None
        }
        json_schema_extra = {
            "example": {
                "linkedin_url": "https://www.linkedin.com/in/example",
                "return_keys": {
                    "first_name": True,
                    "last_name": True,
                    "full_name": True,
                    "headline": True,
                    "about": True,
                    "location": True,
                    "experiences": True,
                    "education": True,
                    "skills": True,
                    "profile_image_url": False
                },
                "filter_empty": True,
                "job_history_count": 2,
                "output_format": "JSON"
            }
        }