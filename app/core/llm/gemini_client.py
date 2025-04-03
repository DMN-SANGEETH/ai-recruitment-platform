import time
from google.api_core import exceptions
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, model, initial_delay=1, max_retries=3, backoff_factor=2):
        self.model = model
        self.initial_delay = initial_delay
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _call_gemini_with_retry(self, prompt: str, domain: str):
        """Call Gemini API with exponential backoff retry logic"""
        delay = self.initial_delay
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                content = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
                return content
            except exceptions.ResourceExhausted as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Rate limit exceeded for {domain} after {self.max_retries} attempts")
                    return None
                logger.warning(f"Rate limit exceeded for {domain}. Retrying in {delay} seconds (attempt {attempt + 1})")
                time.sleep(delay) 
                delay *= self.backoff_factor
            except Exception as e:
                logger.error(f"Unexpected error generating content for {domain}: {str(e)}")
                return None
        return None