# app/utils/logger.py

import logging

logger = logging.getLogger("ai-platform")
logger.setLevel(logging.DEBUG)

# Optional: log to console
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
