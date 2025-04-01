import os
from dotenv import load_dotenv

#Load env
load_dotenv()

def get_mongodb_uri():
    """Get MongoDB conection URI from evn"""
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    host = os.getenv("MONGO_HOST", "localhost")
    port = os.getenv("MONGO_PORT","")

    if user and password:
        return f"mongodb://{user}:{password}@{host}:{port}"
    return f"mongodb://{host}:{port}"

def get_gemini_api_key():
    """Get Gemini API key"""
    return os.getenv("GEMINI_API_KEY")

def get_app_config():
    """Get App configration"""
    return {
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }