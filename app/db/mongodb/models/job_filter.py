from typing import List, Optional, Dict, Union
from pydantic import BaseModel, HttpUrl

class Company(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    employee_range: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[Union[HttpUrl, str]] = None
    website: Optional[Union[HttpUrl, str]] = None
    year_founded: Optional[int] = None
    hq_city: Optional[str] = None
    hq_country: Optional[str] = None
    id: Optional[str] = None
    logo_url: Optional[Union[HttpUrl, str]] = None

class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_id: Optional[str] = None
    company_linkedin_url: Optional[Union[HttpUrl, str]] = None
    company_logo_url: Optional[Union[HttpUrl, str]] = None
    date_range: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    is_current: Optional[bool] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    start_month: Optional[int] = None
    start_year: Optional[int] = None
    end_month: Optional[int] = None
    end_year: Optional[int] = None

class LinkedInProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    profile_id: Optional[str] = None
    headline: Optional[str] = None
    about: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    profile_image_url: Optional[Union[HttpUrl, str]] = None
    public_id: Optional[str] = None
    urn: Optional[str] = None
    linkedin_url: Optional[Union[HttpUrl, str]] = None
    
    # Company information can be either a string or Company object
    company: Optional[Union[str, Company]] = None
    company_domain: Optional[str] = None
    company_employee_range: Optional[str] = None
    company_industry: Optional[str] = None
    company_linkedin_url: Optional[Union[HttpUrl, str]] = None
    company_website: Optional[Union[HttpUrl, str]] = None
    company_year_founded: Optional[int] = None
    hq_city: Optional[str] = None
    hq_country: Optional[str] = None
    
    # Current job details
    current_company_join_month: Optional[Union[int, str]] = None
    current_company_join_year: Optional[Union[int, str]] = None
    current_job_duration: Optional[str] = None
    
    # Work experiences
    experiences: Optional[List[Experience]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "DMN",
                "last_name": "Sangeeth",
                "full_name": "DMN Sangeeth",
                "profile_id": "913371504",
                "headline": "AI/ML Engineer | Software Engineer | Freelancer (AI & ML)",
                "about": "An enthusiastic Information Technology professional...",
                "job_title": "AI/ML Engineer",
                "location": "Colombo District, Western Province, Sri Lanka",
                "city": "Colombo District",
                "country": "Sri Lanka",
                "public_id": "dmn-sangeeth",
                "urn": "ACoAADZw8XABMZkA2xzUlisJkua3pG0HnRQUGDc",
                "linkedin_url": "https://www.linkedin.com/in/dmn-sangeeth/",
                "company": "OXO Tech",
                "company_domain": "oxotech.io",
                "company_employee_range": "11-50",
                "company_industry": "IT Services and IT Consulting",
                "company_linkedin_url": "https://www.linkedin.com/company/oxo-tech",
                "company_website": "http://www.oxotech.io",
                "hq_city": "Colombo",
                "hq_country": "LK",
                "current_company_join_month": 4,
                "current_company_join_year": 2025,
                "current_job_duration": "2 mos",
                "experiences": [
                    {
                        "company": "OXO Tech",
                        "company_id": "104991085",
                        "company_linkedin_url": "https://www.linkedin.com/company/104991085",
                        "company_logo_url": "https://media.licdn.com/...",
                        "date_range": "Apr 2025 - Present",
                        "description": "Skills: Large Language Models...",
                        "duration": "2 mos",
                        "is_current": True,
                        "job_type": "Full-time",
                        "location": "Colombo, LK · Hybrid",
                        "skills": "Large Language Models...",
                        "start_month": 4,
                        "start_year": 2025,
                        "title": "AI/ML Engineer"
                    }
                ]
            }
        }