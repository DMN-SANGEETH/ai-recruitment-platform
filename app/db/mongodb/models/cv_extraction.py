from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Experience(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    title: str
    company: str
    duration: str
    description: str

class Education(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    degree: str
    institution: str
    year: str

class Project(BaseModel):
    name: str
    description: str

class    ResumeResponse(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    certifications: List[str]
    projects: List[Project]
    file_path: str
    is_valid_resume: bool
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        },
        populate_by_name=True
    )