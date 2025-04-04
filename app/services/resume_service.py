from typing import Dict, List
from app.core.llm.resume_processor import ResumeProcessor
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.utils.file_handling import FileHandler
from app.utils.logger import logger


class ResumeService:
    def __init__(self):
        """Initialize the Resume Service"""
        self.processor = ResumeProcessor()
        self.repository = ResumeRepository()

    def process_resume_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, any]:
        """Process resume directly from bytes without saving to disk"""
        try:
            # Extract text directly from bytes
            resume_text = FileHandler.extract_text_from_bytes(file_bytes, filename)
            if not resume_text:
                logger.error("Failed to extract text from file bytes")
                return None
            
            # Process resume data
            resume_data = self.processor.process_resume(resume_text)
            return resume_data

        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return None
        
    def get_resume_by_id(self, resume_id: str) -> Dict[str, any]:
        """Get a resume by ID"""
        try:
            resume = self.repository.find_by_id(resume_id)
            if resume:
                return resume.model_dump()
            return None
        except Exception as e:
            logger.error(f"Error getting resume by ID: {str(e)}")
            return None
    
    def get_all_resumes(self, limit: int = 100, skip: int = 0) -> List[Dict[str, any]]:
        """Get all resumes"""
        try:
            resumes = self.repository.find_many({}, limit=limit, skip=skip)
            return [resume.model_dump() for resume in resumes]
        except Exception as e:
            logger.error(f"Error getting all resumes: {str(e)}")
            return []
    
    def delete_resume(self, resume_id: str) -> bool:
        """Delete a resume and its associated file"""
        try:
            # Get the resume to find its file path
            resume = self.repository.find_by_id(resume_id)
            if not resume:
                logger.error(f"Resume with ID {resume_id} not found")
                return False
            
            # Delete the file if it exists
            if resume.file_path and os.path.exists(resume.file_path):
                try:
                    os.remove(resume.file_path)
                    logger.info(f"Deleted file: {resume.file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete resume file: {str(e)}")
            
            # Delete the resume from the database
            result = self.repository.delete(resume_id)
            return result
            
        except Exception as e:
            logger.error(f"Error deleting resume: {str(e)}")
            return False