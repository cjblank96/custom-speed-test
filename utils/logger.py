import logging
import os
from datetime import datetime

def setup_logger(name="speedtest_logger", log_file="logs/speedtest.log", level=logging.INFO):
    """
    Sets up a logger that logs to both console and file.

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger object
    """
    # Ensure the logs directory exists
    try:
        os.makedirs("logs", exist_ok=True)
    except Exception as e:
        print(f"❌ Failed to create logs directory: {e}")

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File logging
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
    except Exception as e:
        print(f"❌ Failed to create log file handler: {e}")
        file_handler = None

    # Console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if file_handler:
        logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()
