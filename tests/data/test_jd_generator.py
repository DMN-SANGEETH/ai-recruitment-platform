"""Test"""
from app.core.llm.jd_processor import JobDescriptionProcessor

def test_data_transformation():
    """Test data transformation"""
    processor = JobDescriptionProcessor()
    raw_data = {
        "job_title": "Python Developer",
        "technology": ["Python", "Django"],
        "key_responsibilities": ["API development", "Testing"],
        "location": "Remote",
        "experience_level": "Mid-level",
        "education": "Bachelor's Degree",
        "salary_range": {"min": 60000, "max": 90000},
        "posted_date": "2024-04-01",
        "application_deadline": "2024-04-30",
        "apply_url": "https://example.com/apply"
    }
    domain = "Software Engineering"

    result = processor._transform_job_data(raw_data, domain)

    assert isinstance(result, dict)
    assert result["title"] == "Python Developer"
    assert result["technology"] == ["Python", "Django"]
    assert result["responsibilities"] == ["API development", "Testing"]
    assert result["location"] == "Remote"
    assert result["experience_level"] == "Mid-level"
    assert result["education"] == "Bachelor's Degree"
    assert result["salary_range"] == {"min": 60000, "max": 90000}
    assert result["posted_date"] == "2024-04-01"
    assert result["application_deadline"] == "2024-04-30"
    assert result["apply_url"] == "https://example.com/apply"
    assert result["domain"] == domain
