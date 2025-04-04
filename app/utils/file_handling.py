import os
import PyPDF2
import docx
from typing import Tuple
from app.utils.logger import logger

class FileHandler:
    """Utility class for handling file uploads and extractions"""
    
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    UPLOAD_FOLDER = 'storage/resumes'

    @classmethod
    def allowed_file(cls, filename: str) -> bool:
        """Check if the file has an allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def save_file(cls, file, filename: str) -> str:
        """Save the uploaded file to the upload folder"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
            
            # Generate the file path
            file_path = os.path.join(cls.UPLOAD_FOLDER, filename)
            
            # Save the file
            with open(file_path, 'wb') as f:
                f.write(file)
            
            logger.info(f"File saved at: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return ""
    
    @classmethod
    def extract_text_from_file(cls, file_path: str) -> str:
        """Extract text content from various file formats"""
        try:
            file_extension = file_path.rsplit('.', 1)[1].lower()
            
            if file_extension == 'pdf':
                return cls._extract_text_from_pdf(file_path)
            elif file_extension in ['doc', 'docx']:
                return cls._extract_text_from_docx(file_path)
            elif file_extension == 'txt':
                return cls._extract_text_from_txt(file_path)
            else:
                logger.error(f"Unsupported file extension: {file_extension}")
                return ""
        
        except Exception as e:
            logger.error(f"Error extracting text from file: {str(e)}")
            return ""
    
    @classmethod
    def _extract_text_from_pdf(cls, file_path: str) -> str:
        """Extract text from PDF files"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    @classmethod
    def _extract_text_from_docx(cls, file_path: str) -> str:
        """Extract text from DOCX files"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            return ""
    
    @classmethod
    def _extract_text_from_txt(cls, file_path: str) -> str:
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {str(e)}")
            return ""