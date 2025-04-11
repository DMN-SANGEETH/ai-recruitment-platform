"""Gemini client"""
import time
import traceback
from typing import Optional
from google.api_core import exceptions

from app.utils import logger
from app.utils.exceptions import GeminiAPIError,LLMError, GeminiRateLimitError, GeminiContentFilterError

class GeminiClient:
    """Gemini client class"""
    def __init__(self, model, initial_delay=1, max_retries=3, backoff_factor=2):
        self.model = model
        self.initial_delay = initial_delay
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _extract_content(self, response) -> str:
        """Safely extract content from Gemini response with error handling"""
        try:
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                if hasattr(response.candidates[0], 'content'):
                    return response.candidates[0].content.parts[0].text

            raise LLMError(f"Unexpected response structure: {response}")
        except (AttributeError, IndexError) as e:
            raise LLMError(f"Failed to extract content from response: {e}") from e

    def _call_gemini_with_retry(self, prompt: str, domain: str = "general") -> Optional[str]:
        """Call Gemini API with exponential backoff retry logic and improved error handling"""
        delay = self.initial_delay
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)

                if hasattr(response, 'blocked') and response.blocked:
                    block_reason = getattr(response, 'block_reason', 'unknown')
                    raise GeminiContentFilterError(f"Content blocked by Gemini safety filters. Reason: {block_reason}")

                content = self._extract_content(response)

                if attempt > 0:
                    logger.info("Successfully completed %s request after %d attempts",
                                domain,
                                attempt+1
                                )

                return content

            except exceptions.ResourceExhausted as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    logger.error(
                        "Rate limit exceeded for %s after %d attempts: %s",
                        domain, self.max_retries, e
                    )
                    raise GeminiRateLimitError(f"Rate limit exceeded for {domain} after {self.max_retries} attempts") from e

                logger.warning(
                    "Rate limit exceeded for %s. Retrying in %s seconds (attempt %d/%d)",
                    domain, delay, attempt + 1, self.max_retries
                )
                time.sleep(delay)
                delay *= self.backoff_factor

            except exceptions.InvalidArgument as e:
                logger.error("Invalid argument to Gemini API for %s: %s",
                             domain,
                             e,
                             exc_info=True
                             )
                raise GeminiAPIError(f"Invalid argument to Gemini API: {str(e)}") from e

            except exceptions.FailedPrecondition as e:
                logger.error("Failed precondition in Gemini API for %s: %s",
                             domain,
                             e,
                             exc_info=True
                             )
                raise GeminiAPIError(f"Failed precondition in Gemini API: {str(e)}") from e

            except exceptions.Unauthenticated as e:
                logger.error("Authentication failed for Gemini API for %s: %s",
                             domain,
                             e,
                             exc_info=True
                             )
                raise GeminiAPIError(f"Authentication failed for Gemini API: {str(e)}") from e

            except (exceptions.DeadlineExceeded) as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    logger.error(
                        "Gemini API unavailable for %s after %d attempts: %s",
                        domain, self.max_retries, e
                    )
                    raise GeminiAPIError(f"Gemini API unavailable after {self.max_retries} attempts") from e

                logger.warning(
                    "Gemini API unavailable for %s. Retrying in %s seconds (attempt %d/%d)",
                    domain,
                    delay,
                    attempt + 1,
                    self.max_retries
                )
                time.sleep(delay)
                delay *= self.backoff_factor

            except Exception as e:
                error_trace = traceback.format_exc()
                logger.exception(
                    "Unexpected error generating content for %s: %s\n%s",
                    domain, e, error_trace
                )
                raise GeminiAPIError(f"Unexpected error with Gemini API: {str(e)}") from e

        raise GeminiAPIError(f"Failed to get response from Gemini API after {self.max_retries} attempts") from last_error
