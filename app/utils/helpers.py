"""Helpers"""
import json
import re
from typing import Optional

from app.utils.logger import logger

def extract_and_validate_json(text: str) -> Optional[str]:
    """
    Extracts and validates JSON from a string, handling code block
    markers and other potential issues. Returns the cleaned JSON
    string if valid, or None if invalid.
    """
    try:
        cleaned_text = re.sub(r"^```(json)?\s*|```\s*$",
                              "",
                              text.strip(),
                              flags=re.MULTILINE
                              ).strip()

        json.loads(cleaned_text)
        return cleaned_text

    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: %s",
                     e,
                     exc_info=True
                     )
        return None
    except ValueError as e:
        logger.error("Value Error during JSON extraction: %s",
                     e,
                     exc_info=True
                     )
        return None

    except (TypeError, AttributeError) as e:
        logger.error("Type or Attribute Error during JSON extraction: %s",
                     e,
                     exc_info=True
                     )
        return None
