from app.utils.logger import logger

if __name__ == "__main__":
    try:
        # your startup logic
        logger.info("Application started successfully.")
    except Exception as e:
        logger.critical(f"Unhandled exception during startup: {e}")
        raise
