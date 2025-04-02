import os
import json
from typing import List
import google.generativeai as genai
import sys
from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.utils.helpers import extract_json_from_response
from app.utils.logger import logger
from app.utils.config import MongoDBConfig

class JobDescriptionGenerator:
    def __init__(self):
        """Initialize the JobDescriptionGenerator with Gemini"""
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        '''self.model = genai.GenerativeModel("gemini-1.5-pro")'''
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.repository = JobDescriptionRepository()

    def generate_job_descriptions(self, domains: List[str], count_per_domain: int):
        for domain in domains:
            prompt = f"""
            Generate {count_per_domain} realistic job description for the {domain} domain name.
            This is import and Each job description should include:
            - Job title (use field name 'title')
            - {domain} need to include
            - Location (mix of remote and in-person, on-site, hybrid)
            - 5-7 Key responsibilities (use field name 'responsibilities')
            - 5-10 required skills (use field name 'required_skills')
            - Technology requirement
            - Experience level requirement (use field name 'experience_level')
            - Education requirement (use field name 'education')
            - Salary range (as min and max values, use field name 'salary_range')

            Format as a JSON array with each job as an object. *without any Markdown or formatting*.
            """

            response = self.model.generate_content(prompt)
            content = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
            cleaned_content = extract_json_from_response(content)
            try:  
                print("RAW CONTENT:")
                job_descriptions = json.loads(cleaned_content)
                for jd_data in job_descriptions:
                    # Transform the data to match the JobDescription model
                    transformed_data = {
                    "title": jd_data.get("job_title", jd_data.get("title", "")),
                    "domain": domain,
                    "technology":jd_data.get("technology_requirement",[]),
                    "programming_languages":jd_data.get("programming languages requirement",[]),
                    "location": jd_data.get("location", ""),
                    "responsibilities": jd_data.get("key_responsibilities", jd_data.get("responsibilities", [])),
                    "required_skills": jd_data.get("required_skills", []),
                    "experience_level": jd_data.get("experience_level_requirement", jd_data.get("experience_level", "")),
                    "education": jd_data.get("education_requirement", jd_data.get("education", "")),
                    "salary_range": jd_data.get("salary_range", {"min": 0, "max": 0}),
                }
                    jd = JobDescription(**transformed_data)
                    self.repository.create(jd)
                logger.info(f"Successfully stored {len(job_descriptions)} job descriptions for domain: {domain}")    
            except Exception as e:
                logger.error(f"Failed to generate job descriptions for domain: '{domain}': {e}")
                
        return f"Generated {count_per_domain * len(domains)} job descriptions"