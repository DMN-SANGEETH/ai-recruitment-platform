from typing import List, Optional, Dict
from pydantic import Field,EmailStr

from app.db.mongodb.models.base import MongoBaseModel

class Experience(MongoBaseModel):
    title: str
    company: str
    duration: str
    description: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineer",
                "company": "Tech Inc",
                "duration": "2020-2023",
                "description": "Developed and maintained web applications"
            }
        }

class Education(MongoBaseModel):
    degree: str
    institution: str
    year: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "degree": "B.S. Computer Science",
                "institution": "University of Technology",
                "year": "2020"
            }
        }

class Resume(MongoBaseModel):
    name: str
    email: EmailStr
    phone: str
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    certifications: List[str] = []
    projects: List[Dict[str, str]] = []
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None
    file_path: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "skills": ["JavaScript", "Python", "React", "AWS"],
                "experience": [
                    {
                        "title": "Software Engineer",
                        "company": "Tech Inc",
                        "duration": "2020-2023",
                        "description": "Developed and maintained web applications"
                    }
                ],
                "education": [
                    {
                        "degree": "B.S. Computer Science",
                        "institution": "University of Technology",
                        "year": "2020"
                    }
                ],
                "file_path": "storage/resumes/john_doe_resume.pdf"
            },
                "summary": "Experienced software engineer with 3+ years in web development"
            }
        