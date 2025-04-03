import json
from typing import List
import google.generativeai as genai
import time
from google.api_core import exceptions
from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.utils.helpers import extract_and_validate_json
from app.utils.logger import logger
from app.utils.config import MongoDBConfig
from app.core.rag.embeddings import EmbeddingGenerator

class JobDescriptionGenerator:
    def __init__(self):
        """Initialize the JobDescriptionGenerator with Gemini"""
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.repository = JobDescriptionRepository()
        self.embedding = EmbeddingGenerator()

    def generate_job_descriptions(self, domains: List[str], count_per_domain: int):
        """Generate job descriptions for specified domains and store them in MongoDB with embeddings."""
        
        total_generated = 0
        for domain in domains:

            generated_count = 0

            prompt = f"""
            Generate {count_per_domain} realistic job description for the {domain} domain name.
            This is import: Ensure the output is valid JSON. Each job description should be a JSON object with the following keys:
            - Job title (use field name 'title', "title" (string))
            - {domain} need to include
            - Technology requirement (some service providers required for specific {domain}, "technology" (array of strings))
            - Location (mix of remote and in-person, on-site, hybrid,"location" (string))
            - 5-7 Key responsibilities (use field name 'responsibilities',"responsibilities" (array of strings))
            - 5-10 required skills (use field name 'required_skills',"required_skills" (array of strings))
            - Experience level requirement (use field name 'experience_level',"experience_level" (string))
            - Education requirement (use field name 'education',"education" (string))
            - Salary range (as min and max values, use field name 'salary_range')

            Format as a JSON array with each job as an object. *Do not include any Markdown or formatting outside of the JSON.*
            """

            retries = 3
            delay = 5  # Initial delay in seconds

            while retries > 0:
                try:
                    response = self.model.generate_content(prompt)
                    content = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
                    cleaned_content = extract_and_validate_json(content)

                    if cleaned_content:
                        print("RAW CONTENT:")
                        job_descriptions = json.loads(cleaned_content)
                        for jd_data in job_descriptions:
                            try:
                                transformed_data = {
                                    "title": jd_data.get("job_title", jd_data.get("title", "")),
                                    "domain": domain,
                                    "technology": jd_data.get("technology_requirement", []),
                                    "location": jd_data.get("location", ""),
                                    "responsibilities": jd_data.get("key_responsibilities", jd_data.get("responsibilities", [])),
                                    "required_skills": jd_data.get("required_skills", []),
                                    "experience_level": jd_data.get("experience_level_requirement", jd_data.get("experience_level", "")),
                                    "education": jd_data.get("education_requirement", jd_data.get("education", "")),
                                    "salary_range": jd_data.get("salary_range", {"min": 0, "max": 0}),
                                }
                                embedding = self.embedding.create_job_description_embedding(transformed_data)
                                transformed_data["embedding"] = embedding
                                jd = JobDescription(**transformed_data)
                                result = self.repository.create(jd)
                                if result:
                                        generated_count += 1
                                        logger.debug(f"Stored job description: {transformed_data['title']}")
                            except Exception as e:
                                logger.error(f"Failed to process job description: {e}")
                                continue

                        logger.info(f"Successfully stored {len(job_descriptions)} job descriptions for domain: {domain}")
                        total_generated += generated_count
                        break 
                    else:
                        logger.error(f"Failed to extract valid JSON for domain: {domain}")
                        break

                except exceptions.ResourceExhausted as e:
                    logger.warning(f"Rate limit exceeded for {domain}. Retrying in {delay} seconds.")
                    time.sleep(delay)
                    delay *= 2 
                    retries -= 1
                except Exception as e:
                    logger.error(f"Failed to generate job descriptions for domain: '{domain}': {e}")
                    break

            if retries == 0:
                logger.error(f"Failed to generate job descriptions for {domain} after multiple retries.")
                
        return f"Generated {total_generated} job descriptions"