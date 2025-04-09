import os
from dotenv import load_dotenv
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from app.utils import logger

load_dotenv()

def get_secret(key: str, default: str = None):
    """Unified method to get secrets from Streamlit or environment variables."""
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)


class MongoDBConfig:

    @staticmethod
    def get_mongodb_uri()-> str:
        """Get MongoDB Atlas connection URI"""
        #uri = os.getenv("MONGO_URI")
        uri = get_secret("MONGO_URI")
        if not uri:
            logger.error("MONGO_URI not set in environment variables")
            raise ConfigurationError("MongoDB connection URI is required")
        return uri

    @staticmethod
    def get_gemini_api_key()-> str:
        """Get Gemini API key with validation"""
        #key = os.getenv("GEMINI_API_KEY")
        key = get_secret("GEMINI_API_KEY")
        if not key:
            logger.error("GEMINI_API_KEY not set in environment variables")
            raise ConfigurationError("Gemini API key is required")
        return key

    @staticmethod
    def get_app_config()-> dict:
        """Get App configuration"""
        return {
            "debug": str(get_secret("DEBUG", "False")).lower() == "true",
            "log_level": get_secret("LOG_LEVEL", "INFO"),
        }

    @staticmethod
    def get_mongodb_connection() -> MongoClient:
        """Establish and return MongoDB Atlas connection"""
        mongo_uri = MongoDBConfig.get_mongodb_uri()
        try:
            client = MongoClient(mongo_uri, tls=True)
            # Verify connection
            client.admin.command('ping')
            logger.info("Successfully connected to MongoDB Atlas")
            return client
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise


if __name__ == "__main__":
    logger.info("Testing MongoDB configuration")
    try:
        logger.info(f"Gemini API Key: {'*' * 8}{MongoDBConfig.get_gemini_api_key()[-4:]}")
        logger.info(f"MongoDB URI: {MongoDBConfig.get_mongodb_uri()[:20]}...")
        logger.info(f"App Config: {MongoDBConfig.get_app_config()}")
        connection = MongoDBConfig.get_mongodb_connection()
        logger.info("MongoDB connection test successful")
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        raise