import logging
import os
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
        # Ensure 'protocol' is always present to prevent KeyError
        if not hasattr(record, 'protocol'):
            record.protocol = "N/A"
        color = self.COLORS.get(record.levelno, self.RESET)
        return f"{color}{super().format(record)}{self.RESET}"

def setup_logger(name="speedtest_logger", log_file="logs/speedtest.log", level=logging.INFO, debug_mode=False):
    """Sets up the logger with log rotation, color-coded console output, and protocol tagging."""
    
    os.makedirs("logs", exist_ok=True)

    # Formatter with protocol context
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(protocol)s] - %(message)s')
    color_formatter = ColorFormatter('%(asctime)s - %(levelname)s - [%(protocol)s] - %(message)s')

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Console handler with color formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # Configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug_mode else level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Proper logging functions to include 'protocol'
    def info(msg, protocol="TCP"):
        logger._log(logging.INFO, msg, args=(), extra={"protocol": protocol})

    def warning(msg, protocol="TCP"):
        logger._log(logging.WARNING, msg, args=(), extra={"protocol": protocol})

    def error(msg, protocol="TCP"):
        logger._log(logging.ERROR, msg, args=(), extra={"protocol": protocol})

    def debug(msg, protocol="TCP"):
        logger._log(logging.DEBUG, msg, args=(), extra={"protocol": protocol})

    # Replace original logging methods with protocol-aware versions
    logger.info = info
    logger.warning = warning
    logger.error = error
    logger.debug = debug

    return logger

# Initialize the logger
logger = setup_logger(debug_mode=False)