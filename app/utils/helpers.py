import re
import json
from app.utils.logger import logger

def extract_and_validate_json(text: str) -> str or None: # type: ignore
    """
    Extracts and validates JSON from a string, handling code block markers and other potential issues.
    Returns the cleaned JSON string if valid, or None if invalid.
    """
    try:
        # Clean the text
        cleaned_text = re.sub(r"^```(json)?\s*|```\s*$", "", text.strip(), flags=re.MULTILINE).strip()

        # Attempt to parse as JSON
        json.loads(cleaned_text) #if this line does not throw an error, then it is valid json.
        return cleaned_text

    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error during JSON extraction: {e}")
        return None