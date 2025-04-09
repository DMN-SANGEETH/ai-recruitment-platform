# # app/utils/logger.py

# import logging

# logger = logging.getLogger("ai-platform")
# logger.setLevel(logging.DEBUG)

# # Optional: log to console
# console_handler = logging.StreamHandler()
# formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
# console_handler.setFormatter(formatter)

# logger.addHandler(console_handler)


import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# This ensures all standard logging methods are available:
# logger.debug(), logger.info(), logger.warning(), logger.error(), logger.critical()

# If you need to export specific functions for backward compatibility
debug = logger.debug
info = logger.info
warning = logger.warning
warn = logger.warning  # Alias
error = logger.error
critical = logger.critical
exception = logger.exception