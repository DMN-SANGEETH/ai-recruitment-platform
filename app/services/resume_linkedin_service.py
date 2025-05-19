"""resume and linkedin Service"""
import os
from typing import Dict, List

from app.core.llm.resume_linkedin_processor import ResumeLinkedinProcessor
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.utils.exceptions import FileProcessingError
from app.utils.file_handling import FileHandler
from app.utils.logger import logger


class ResumeLinkedinService:
    """Resume Service"""
    def __init__(self):
        """Initialize the Resume Service"""
        self.processor = ResumeLinkedinProcessor()
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
                print("type===================================",type(resume_text))
                print("resume_text doing OCR 1 ===================================",resume_text)
            except FileProcessingError as e:
                logger.error(f"Text extraction failed: {str(e)}")
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
            resume_data = await self.processor.process_resume_linkedin(resume_text, file_path)
            print("resume_data type===================================",type(resume_data))
            print("after proceing 2 resume_data:",resume_data)
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