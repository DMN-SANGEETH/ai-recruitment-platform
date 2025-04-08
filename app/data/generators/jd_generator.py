import json
from typing import List
import google.generativeai as genai
import time
from google.api_core import exceptions
from app.core.llm.prompt_template import JD_GENERATION_TEMPLATE
from app.db.mongodb.models.job_description import JobDescription
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.utils.helpers import extract_and_validate_json
from app.utils.logger import logger
from app.utils.config import MongoDBConfig
from app.core.rag.embeddings import EmbeddingGenerator
from app.core.llm.jd_processor import JobDescriptionProcessor
from app.core.llm.gemini_client import GeminiClient

class JobDescriptionGenerator:
    def __init__(self):
        """Initialize the JobDescriptionGenerator with Gemini"""
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        model = genai.GenerativeModel("gemini-1.5-flash") #gemini-1.5-flash gemini-1.5-pro

        self.gemini_client = GeminiClient(
            model=model,
            initial_delay=5,
            max_retries=3,
            backoff_factor=2
        )

        self.repository = JobDescriptionRepository()
        self.embedding = EmbeddingGenerator()
        self.job_processor = JobDescriptionProcessor()

    def _generate_prompt(self, domain: str, count: int):
        """Generate job descriptions for specified domains and store them in MongoDB with embeddings."""
        return JD_GENERATION_TEMPLATE.format(
            domain=domain,
            count=count
        )

    def generate_job_descriptions(self, domains: List[str], count_per_domain: int):
        """Generate job descriptions for specified domains and store them in MongoDB"""
        if not domains or count_per_domain <= 0:
            return "No domains specified or invalid count per domain"

        total_generated = 0

        for domain in domains:
            logger.info(f"Processing domain: {domain}")
            time.sleep(20)

            prompt = self._generate_prompt(domain, count_per_domain)
            content = self.gemini_client._call_gemini_with_retry(prompt, domain)

            if not content:
                continue

            try:
                cleaned_content = extract_and_validate_json(content)
                if not cleaned_content:
                    logger.error(f"Invalid JSON content for domain: {domain}")
                    continue

                job_descriptions = json.loads(cleaned_content)

                if not isinstance(job_descriptions, list):
                    job_descriptions = [job_descriptions]

                generated_count = self.job_processor.process_job_descriptions(domain, job_descriptions)
                total_generated += generated_count
                logger.info(f"Successfully processed {generated_count} job descriptions for {domain}")

            except Exception as e:
                logger.error(f"Failed to process job descriptions for {domain}: {str(e)}")
                continue
        return f"Successfully generated {total_generated} job descriptions across {len(domains)} domains"