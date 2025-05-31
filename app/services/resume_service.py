"""Resume Service"""
import os
from typing import Dict, List

from app.core.llm.resume_processor import ResumeProcessor
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.utils.exceptions import FileProcessingError
from app.utils.file_handling import FileHandler
from app.utils.logger import logger


class ResumeService:
    """Resume Service"""
    def __init__(self):
        """Initialize the Resume Service"""
        self.processor = ResumeProcessor()
        self.repository = ResumeRepository()

    async def process_resume_file(self, file, filename: str) -> Dict[str, any]:
        """Process resume file with robust error handling"""
        try:
            # Save file
            file_path = await FileHandler.save_file(file, filename)
            if not file_path:
                logger.error("Failed to save resume file")
                return {
                    "error": "Failed to save file",
                    "success": False
                }

            # Extract content with multiple attempts
            try:
                resume_text = await FileHandler.extract_text_doing_ocr(file_path)
            except FileProcessingError as e:
                logger.error("Text extraction failed: %s", {str(e)})
                return {
                    "error": str(e),
                    "success": False,
                    "recoverable": True  # Indicates retry might help
                }

            if not resume_text:
                logger.error("Empty text extracted from resume")
                return {
                    "error": "No text extracted",
                    "success": False
                }

            # Process resume data
            resume_data = await self.processor.extract_resume(resume_text, file_path)
            if not resume_data:
                logger.error("Failed to process resume data")
                return {
                    "error": "Resume processing failed",
                    "success": False
                }

            return {
                "data": resume_data,
                "success": True
            }

        except Exception as e:
            logger.error(f"Unexpected error processing resume: {str(e)}", exc_info=True)
            return {
                "error": "Internal server error",
                "success": False
            }


    def process_resume_bytes(self,
                             file_bytes: bytes,
                             filename: str
                             ) -> Dict[str, any]:
        """Process resume directly from bytes without saving to disk"""
        try:
            # Extract text directly from bytes
            resume_text = FileHandler._extract_text_from_pdf_bytes(file_bytes)
            if not resume_text:
                logger.error("Failed to extract text from file bytes")
                return None

            # Process resume data
            resume_data = self.processor.process_resume(resume_text, filename)
            return resume_data

        except Exception as e:
            logger.error("Error processing resume data: %s", e)
            return None

    def get_resume_by_id(self,
                         resume_id: str
                         ) -> Dict[str, any]:
        """Get a resume by ID"""
        try:
            resume = self.repository.find_by_id(resume_id)
            if resume:
                return resume.model_dump()
            return None

        except Exception as e:
            logger.error("Error getting resume by ID: %s", e)
            return None

    def get_all_resumes(self,
                        limit: int = 100,
                        skip: int = 0
                        ) -> List[Dict[str, any]]:
        """Get all resumes"""
        try:
            resumes = self.repository.find_many({}, limit=limit, skip=skip)
            return [resume.model_dump() for resume in resumes]

        except Exception as e:
            logger.error("Error getting all resumes: %s", e)
            return []

    def delete_resume(self,
                      resume_id: str
                      ) -> bool:
        """Delete a resume and its associated file"""
        try:
            # Get the resume to find its file path
            resume = self.repository.find_by_id(resume_id)
            if not resume:
                logger.error("Resume with ID %s not found", resume_id)
                return False

            # Delete the file if it exists
            if resume.file_path and os.path.exists(resume.file_path):
                try:
                    os.remove(resume.file_path)
                    logger.info("Deleted file: %s", resume.file_path)

                except Exception as e:
                    logger.error("Failed to delete resume file: %s", e)

            # Delete the resume from the database
            result = self.repository.delete(resume_id)
            return result

        except Exception as e:
            logger.error("Error deleting resume: %s", e, exc_info=True)
            return False
