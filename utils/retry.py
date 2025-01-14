import time
from functools import wraps
from utils.logger import logger

def retry(exceptions, tries=3, delay=2, backoff=2):
    """
    Retry decorator for handling transient errors.

    Args:
        exceptions: Exception types to catch
        tries: Total number of attempts
        delay: Initial delay between retries
        backoff: Multiplier for delay increase

    Usage:
        @retry((ConnectionError, TimeoutError), tries=3)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{func.__name__} failed: {e}. Retrying in {_delay}s...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            # Final attempt
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.error(f"{func.__name__} failed after {tries} attempts: {e}")
                return None
        return wrapper
    return decorator
