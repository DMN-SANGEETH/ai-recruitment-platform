"""File Handler"""
import os
from io import BytesIO
import PyPDF2
import docx


from app.utils.exceptions import FileHandlingError
from app.utils.logger import logger

class FileHandler:
    """Utility class for handling file uploads and extractions"""

    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    UPLOAD_FOLDER = 'storage/resumes'

    @classmethod
    def allowed_file(cls,
                     filename: str
                     ) -> bool:
        """Check if the file has an allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    @classmethod
    def save_file(cls,
                  file, filename: str
                  ) -> str:
        """Save the uploaded file to the upload folder"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

            # Generate the file path
            file_path = os.path.join(cls.UPLOAD_FOLDER, filename)

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(file)

            logger.info("File saved at: %s", file_path)
            return file_path

        except IOError as e:
            logger.error("Failed to save file %s: %s",
                        file_path,
                        e,
                        exc_info=True
                        )
            return None

    @classmethod
    def extract_text_from_bytes(cls,
                                file_bytes: bytes,
                                filename: str
                                ) -> str:
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
                logger.error("Unsupported file extension: %s",
                             file_extension
                             )
                return None

        except (TypeError, ValueError, UnicodeDecodeError) as e:
            logger.error("Failed to extract text from %s: %s",
                        filename,
                        e,
                        exc_info=True
                        )
            return None

        except FileHandlingError as e:
            logger.error("Unexpected error processing %s: %s",
                        filename,
                        e,
                        exc_info=True
                        )
            return None

    @classmethod
    def _extract_text_from_pdf_bytes(cls,
                                     file_bytes: bytes
                                     ) -> str:
        """Extract text from PDF bytes"""
        try:
            text = ""
            with BytesIO(file_bytes) as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text

        except ValueError as e:
            logger.error("PDF extraction error: %s",
                         e,
                         exc_info=True
                         )
            return ""

    @classmethod
    def _extract_text_from_docx_bytes(cls,
                                      file_bytes: bytes
                                      ) -> str:
        """Extract text from DOCX bytes"""
        try:
            with BytesIO(file_bytes) as docx_file:
                doc = docx.Document(docx_file)
                return "\n".join([para.text for para in doc.paragraphs])

        except ValueError as e:
            logger.error("DOCX extraction error: %s",
                         e,
                         exc_info=True
                         )
            return ""

    @classmethod
    def _extract_text_from_txt(cls, file_path: str) -> str:
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        except FileNotFoundError:
            logger.error("Text file not found: %s", file_path)
            raise

        except OSError as e:
            logger.error("Error reading text file %s: %s", file_path, e, exc_info=True)
            raise
