import pytest
from app.core.llm.jd_processor import JobDescriptionProcessor

def test_data_transformation():
    processor = JobDescriptionProcessor()
    raw_data = {
        "job_title": "Python Developer",
        "technology": ["Python", "Django"],
        "key_responsibilities": ["API development", "Testing"]
    }