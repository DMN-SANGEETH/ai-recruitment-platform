# app/utils/exceptions.py

class RecruitmentError(Exception):
    """Base exception for all recruitment platform errors"""

class LLMError(RecruitmentError):
    """Errors related to LLM operations"""

class DataProcessingError(RecruitmentError):
    """Errors related to data processing and transformation"""

class DatabaseError(RecruitmentError):
    """Errors related to database operations"""

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

