import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class ColorFormatter(logging.Formatter):
    """Custom log formatter with color-coded output for console."""

    COLORS = {
        logging.DEBUG: "\033[94m",    # Blue
        logging.INFO: "\033[92m",     # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",    # Red
        logging.CRITICAL: "\033[95m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

def setup_logger(name="speedtest_logger", log_file="logs/speedtest.log", level=logging.INFO, debug_mode=False):
    """Sets up a logger with log rotation, color-coded console output, and protocol tagging.

    Args:
        name: Logger name.
        log_file: Path to log file.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        debug_mode: Enable verbose debugging output.

    Returns:
        Configured logger object.
    """
    # Ensure the logs directory exists
    try:
        os.makedirs("logs", exist_ok=True)
    except Exception as e:
        print(f"❌ Failed to create logs directory: {e}")

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(protocol)s] - %(message)s')
    color_formatter = ColorFormatter('%(asctime)s - %(levelname)s - [%(protocol)s] - %(message)s')

    # File logging with rotation (max 5 MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Console logging with color coding
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug_mode else level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Add protocol-aware logging methods
    def info(msg, protocol="TCP"):
        logger.info(msg, extra={"protocol": protocol})

    def warning(msg, protocol="TCP"):
        logger.warning(msg, extra={"protocol": protocol})

    def error(msg, protocol="TCP"):
        logger.error(msg, extra={"protocol": protocol})

    def debug(msg, protocol="TCP"):
        logger.debug(msg, extra={"protocol": protocol})

    # Attach protocol-aware methods
    logger.info = info
    logger.warning = warning
    logger.error = error
    logger.debug = debug

    return logger

# Initialize the logger with debug mode off by default
logger = setup_logger(debug_mode=False)