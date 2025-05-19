class LinkedInValidation:
    """validation for linkedin"""
    def __init__(self):
        """validation"""

    @staticmethod
    def validate_linkedin_url_pr(url):
        """Validate LinkedIn URL format"""
        valid_prefixes = (
            "https://www.linkedin.com/in/",
            "http://www.linkedin.com/in/",
            "https://linkedin.com/in/",
            "http://linkedin.com/in/"
        )
        return any(url.startswith(prefix) for prefix in valid_prefixes)
