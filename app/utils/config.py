"""Configurations"""
import os
from typing import List
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

class Settings:
    """Application settings class"""

    @staticmethod
    def get_allowed_hosts() -> List[str]:
        """Get allowed hosts for CORS"""
        hosts = get_secret("ALLOWED_HOSTS", "http://localhost:8501,http://localhost:8000")
        return [host.strip() for host in hosts.split(",") if host.strip()]

class LinkedInConfig:
    """LinkedIn Config"""

    @staticmethod
    def get_relevance_ai_api_key() -> str:
        """Get RELEVANCE AI API Key"""
        key = get_secret("RELEVANCE_API_KEY")
        if not key:
            logger.error("RELEVANCE_API_KEY not set in environment variables")
            raise ConfigurationError("RELEVANCE_API_KEY is required")
        return key

    @staticmethod
    def get_relevance_ai_project_id() -> str:
        """Get RELEVANCE__PROJECT_ID"""
        endpoint = get_secret("RELEVANCE__PROJECT_ID")
        if not endpoint:
            logger.error("RELEVANCE__PROJECT_ID not set in environment variables")
            raise ConfigurationError("RELEVANCE__PROJECT_ID is required")
        return endpoint

    @staticmethod
    def get_relevance_ai_endpoint() -> str:
        """Get RELEVANCE__ENDPOINT"""
        project_id = get_secret("RELEVANCE__ENDPOINT")
        if not project_id:
            logger.error("RELEVANCE__ENDPOINT not set in environment variables")
            raise ConfigurationError("RELEVANCE__ENDPOINT is required")
        return project_id

    @staticmethod
    def get_relevance_ai_api_timeout() -> str:
        """Get RELEVANCE__API_TIMEOUT"""
        api_timeout = get_secret("RELEVANCE__API_TIMEOUT")
        if not api_timeout:
            logger.error("RELEVANCE__API_TIMEOUT not set in environment variables")
            raise ConfigurationError("RELEVANCE__API_TIMEOUT is required")
        return api_timeout

class MongoDBConfig:
    """Mongo DB Config class"""

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
            logger.error("Failed to connect to MongoDB Atlas: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error connecting to MongoDB: %s", e)
            raise


if __name__ == "__main__":
    logger.info("Testing MongoDB configuration")
    try:
        logger.info("Gemini API Key: %s%s", '*' * 8, MongoDBConfig.get_gemini_api_key()[-4:])
        logger.info("MongoDB URI: %s...", MongoDBConfig.get_mongodb_uri()[:20])
        logger.info("App Config: %s", MongoDBConfig.get_app_config())
        connection = MongoDBConfig.get_mongodb_connection()
        logger.info("MongoDB connection test successful")
    except Exception as e:
        logger.error("Configuration test failed: %s", e)
        raise
