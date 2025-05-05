"""File Handler"""
import os
from io import BytesIO
import PyPDF2
import docx
from google import genai


from app.core.llm.gemini_client import GeminiClient
from app.utils.config import MongoDBConfig
from app.utils.exceptions import FileProcessingError
from app.utils.logger import logger

class FileHandler:
    """Utility class for handling file uploads and extractions"""

    ALLOWED_EXTENSIONS = {'py', 'java', 'cpp', 'c', 'h', 'cs', 'js', 'html', 'css', 'php', 'sh', 'bat', 'go', 'rb', 'swift', 'kt', 'ts', 'json', 'xml', 'yml', 'yaml', 'sql', 'md','txt', 'rtf', 'doc', 'docx', 'odt', 'pdf','pdf', 'docx', 'doc', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'web', 'xls', 'xlsx', 'ods', 'csv', 'tsv', 'epub', 'mobi', 'azw', 'fb2'}
    UPLOAD_FOLDER = 'storage/resumes'

    @classmethod
    def allowed_file(cls,
                     filename: str
                     ) -> bool:
        """Check if the file has an allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    @classmethod
    async def save_file(cls, file, filename: str) -> str:
        """Save the uploaded file to the upload folder"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
            # Generate the file path
            file_path = os.path.join(cls.UPLOAD_FOLDER, filename)

            # Handle different file types
            if hasattr(file, 'getvalue'):  # Streamlit file
                file_content = file.getvalue()
            elif hasattr(file, 'read'):  # FastAPI UploadFile
                file_content = await file.read()
            else:
                file_content = file  # Assume it's already bytes

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            logger.info("File saved at: %s", file_path)
            return file_path
        except Exception as e:
            logger.error("Failed to save file %s: %s", file_path, e, exc_info=True)
            raise FileProcessingError(f"Failed to save file: {str(e)}")

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
                error_msg = "Unsupported file extension: %s",file_extension
                logger.error(error_msg)
                raise FileProcessingError(error_msg)

        except (TypeError, ValueError, UnicodeDecodeError) as e:
            logger.error("Failed to extract text from %s: %s",
                        filename,
                        e,
                        exc_info=True
                        )
            raise FileProcessingError(f"Failed to extract text from {filename}: {str(e)}") from e

    @classmethod
    async def extract_text_doing_ocr(cls, file_path: str) -> str:
        """Simplified extraction matching your working example"""
        try:
            client = genai.Client(api_key=MongoDBConfig.get_gemini_api_key())
            uploaded_file = client.files.upload(file=file_path)

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, "Extract all text exactly as it appears:"]
            )

            if hasattr(response, 'text'):
                return response.text
            if hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text

            raise FileProcessingError("Unexpected response format")

        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            raise FileProcessingError(f"Text extraction failed: {str(e)}")

    @classmethod
    def _extract_text_from_pdf_bytes(cls,
                                     file_bytes: bytes,
                                     ) -> str:
        """Extract text from PDF bytes"""
        try:
            text = ""
            with BytesIO(file_bytes) as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text

        except Exception as e:
            logger.error("PDF extraction error: %s",
                         e,
                         exc_info=True
                         )
            raise FileProcessingError(f"Error extracting text from DOCX: {str(e)}") from e

    @classmethod
    def _extract_text_from_docx_bytes(cls,
                                      file_bytes: bytes
                                      ) -> str:
        """Extract text from DOCX bytes"""
        try:
            with BytesIO(file_bytes) as docx_file:
                doc = docx.Document(docx_file)
                return "\n".join([para.text for para in doc.paragraphs])

        except Exception as e:
            logger.error("DOCX extraction error: %s",
                         e,
                         exc_info=True
                         )
            raise FileProcessingError(f"Error extracting text from DOCX: {str(e)}") from e

    @classmethod
    def _extract_text_from_txt(cls, file_path: str) -> str:
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        except FileNotFoundError as e:
            logger.error("Text file not found: %s", file_path)
            raise FileProcessingError(f"Text file not found: {file_path}") from e

        except OSError as e:
            logger.error("Error reading text file %s: %s", file_path, e, exc_info=True)
            raise FileProcessingError(f"Error reading text file: {str(e)}") from e
