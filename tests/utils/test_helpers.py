from app.utils.helpers import extract_and_validate_json

def test_valid_json_with_codeblocks():
    input_text = """```json
    [{"title":"Backend Engineer"}]'''
    """
    result = extract_and_validate_json(input_text)
    assert result == '[{"title":"Backend Engineer"}]'

def test_invalid_json():
    input_text = """```json
    {"title": "Developer",}```  # Trailing comma
    """
    assert extract_and_validate_json(input_text) is None

def test_non_json_content():
    assert extract_and_validate_json("Just plain text") is None