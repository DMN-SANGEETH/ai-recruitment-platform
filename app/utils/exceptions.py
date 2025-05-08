# app/utils/exceptions.py

"""
Custom Exceptions Module
Defines all application-specific exceptions for better error handling
"""

from fastapi import status

class BaseApplicationError(Exception):
    """Base exception for all application errors"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An unexpected error occurred"
    
    def __init__(self, detail: str = None, status_code: int = None):
        """
        Initialize exception with optional custom detail and status code
        
        Args:
            detail: Custom error message
            status_code: HTTP status code
        """
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code
        super().__init__(self.detail)

class ConfigurationError(BaseApplicationError):
    """Exception for configuration errors"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Application configuration error"

class DatabaseError(BaseApplicationError):
    """Exception for database errors"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Database operation failed"

class ValidationError(BaseApplicationError):
    """Exception for data validation errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Data validation failed"

class ResourceNotFoundError(BaseApplicationError):
    """Exception for resource not found errors"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"

class AuthenticationError(BaseApplicationError):
    """Exception for authentication errors"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication failed"

class AuthorizationError(BaseApplicationError):
    """Exception for authorization errors"""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not authorized to access this resource"

# LinkedIn-specific exceptions

class LinkedInAPIError(BaseApplicationError):
    """Exception for LinkedIn API errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "LinkedIn API request failed"

class ProfileProcessingError(BaseApplicationError):
    """Exception for LinkedIn profile processing errors"""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Failed to process LinkedIn profile"

class ProfileValidationError(ValidationError):
    """Exception for LinkedIn profile validation errors"""
    detail = "LinkedIn profile validation failed"

class TimeoutError(BaseApplicationError):
    """Exception for request timeout errors"""
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    detail = "Request timed out"

class FileUploadError(BaseApplicationError):
    """Exception for file upload errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "File upload failed"


class RecruitmentError(Exception):
    """Base exception for all recruitment platform errors"""

class LLMError(RecruitmentError):
    """Errors related to LLM operations"""

class DataProcessingError(RecruitmentError):
    """Errors related to data processing and transformation"""


class EmbeddingError(RecruitmentError):
    """Errors related to embedding generation"""

# More specific exceptions
class GeminiAPIError(LLMError):
    """Errors from the Gemini API"""

class JSONParsingError(DataProcessingError):
    """Errors during JSON parsing"""

class JobDescriptionProcessingError(DataProcessingError):
    """Errors during job description processing"""

class GeminiRateLimitError(GeminiAPIError):
    """Rate limit exceeded error from Gemini API"""

class GeminiContentFilterError(GeminiAPIError):
    """Content was filtered by Gemini safety filters"""

class StoreJobDescription(Exception):
    """Job data storing error"""

class GetCountOfFailures(Exception):
    """Get Count Of Failures"""

class GetCountError(Exception):
    """Get count error"""

class FileHandlingError(Exception):
    """File unexpected error processing"""

# Resume process

class FileProcessingError(Exception):
    """Raised when there's an error processing a file"""

class ResumeProcessingError(Exception):
    """Raised when there's an error processing a resume"""

