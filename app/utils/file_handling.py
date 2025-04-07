import os
import PyPDF2
import docx
from io import BytesIO
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
    def extract_text_from_bytes(cls, file_bytes: bytes, filename: str) -> str:
        """Extract text directly from file bytes"""
        try:
            file_extension = filename.rsplit('.', 1)[1].lower()

            if file_extension == 'pdf':
                return cls._extract_text_from_pdf_bytes(file_bytes)
            elif file_extension in ['doc', 'docx']:
                return cls._extract_text_from_docx_bytes(file_bytes)
            elif file_extension == 'txt':
                return file_bytes.decode('utf-8')
            else:
                logger.error(f"Unsupported file extension: {file_extension}")
                return ""

        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""

    @classmethod
    def _extract_text_from_pdf_bytes(cls, file_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            text = ""
            with BytesIO(file_bytes) as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return ""

    @classmethod
    def _extract_text_from_docx_bytes(cls, file_bytes: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            with BytesIO(file_bytes) as docx_file:
                doc = docx.Document(docx_file)
                return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            logger.error(f"DOCX extraction error: {str(e)}")
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