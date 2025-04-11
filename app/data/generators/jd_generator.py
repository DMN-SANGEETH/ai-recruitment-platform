"""JD Generate component"""
import json
import time
from typing import List
import google.generativeai as genai

from app.core.llm.prompt_template import JD_GENERATION_TEMPLATE
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.utils.exceptions import GeminiAPIError, GeminiContentFilterError, GeminiRateLimitError, GetCountError, LLMError
from app.utils.helpers import extract_and_validate_json
from app.utils.logger import logger
from app.utils.config import MongoDBConfig
from app.core.rag.embeddings import EmbeddingGenerator
from app.core.llm.jd_processor import JobDescriptionProcessor
from app.core.llm.gemini_client import GeminiClient

class JobDescriptionGenerator:
    """Job Description Generation"""
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

    def _generate_prompt(self,
                         domain: str,
                         count: int
                         ):
        """
        Generate job descriptions for specified domains and store them in
        MongoDB with embeddings.
        """
        return JD_GENERATION_TEMPLATE.format(
            domain=domain,
            count=count
        )

    def generate_job_descriptions(self,
                                  domains: List[str],
                                  count_per_domain: int
                                  ):
        """Generate job descriptions for specified domains and store them in MongoDB"""
        if not domains or count_per_domain <= 0:
            return "No domains specified or invalid count per domain"

        total_generated = 0

        for domain in domains:

            try:

                logger.info("Processing domain: %s", domain)
                time.sleep(20)

                prompt = self._generate_prompt(domain, count_per_domain)
                try:
                    content = self.gemini_client._call_gemini_with_retry(prompt, domain)
                except GeminiRateLimitError as e:
                    logger.error("Rate limit exceeded for domain %s: %s", domain, e)
                    time.sleep(60)
                    continue

                except GeminiContentFilterError as e:
                    logger.error("Content filtered for domain %s: %s", domain, e)
                    continue

                except GeminiAPIError as e:
                    logger.error("Gemini API error for domain %s: %s", domain, e)
                    continue

                except LLMError as e:
                    logger.error("LLM general error for domain %s: %s", domain, e)
                    continue

                if not content:
                    logger.warning("Empty content returned for domain: %s", domain)
                    continue

                cleaned_content = extract_and_validate_json(content)

                if not cleaned_content:
                    logger.error("Invalid JSON content for domain: %s", domain)
                    continue

                try:
                    job_descriptions = json.loads(cleaned_content)

                except json.JSONDecodeError as e:
                    logger.error("JSON parsing error for domain %s: %s", domain, e)
                    continue

                if not isinstance(job_descriptions, list):
                    job_descriptions = [job_descriptions]
                    logger.info("Converted single job description to list for domain: %s", domain)

                try:

                    generated_count = self.job_processor.process_job_descriptions(domain,
                                                                                    job_descriptions
                                                                                    )
                    total_generated += generated_count['success']
                    logger.info("Successfully processed %d job descriptions for %s",
                                generated_count['success'],  # Access the 'success' count
                                domain)

                except GetCountError as e:
                    logger.error("Failed to process job descriptions for %s: %s",
                                domain,
                                e
                                )
                    continue

            except KeyError as e:
                logger.error("Key error processing domain %s: %s", domain, e)
                continue

            except TypeError as e:
                logger.error("Type error processing domain %s: %s", domain, e)
                continue

        result_msg = f"Successfully generated {total_generated} job descriptions across {len(domains)} domains"
        logger.info(result_msg)
        return result_msg
