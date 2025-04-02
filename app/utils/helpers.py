import re

def extract_json_from_response(text: str) -> str:
    # Strip out ```json and ``` if present
    cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned.strip()