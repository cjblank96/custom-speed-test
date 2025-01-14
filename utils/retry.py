import time
from functools import wraps
from utils.logger import logger

def retry(exceptions, tries=3, delay=2, backoff=2, timeout=None, on_failure=None, protocol="TCP"):
    """Retry decorator for handling transient errors with protocol awareness and timeout.

    Args:
        exceptions: Exception types to catch.
        tries: Total number of retry attempts.
        delay: Initial delay between retries (in seconds).
        backoff: Factor to multiply delay after each failure.
        timeout: Maximum total time to keep retrying (in seconds). Optional.
        on_failure: Optional callback function to execute after all retries fail.
        protocol: Protocol used in the operation (TCP/UDP/HTTP3).

    Usage:
        @retry((ConnectionError, TimeoutError), tries=3, protocol="UDP")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            start_time = time.time()

            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    elapsed_time = time.time() - start_time
                    if timeout and elapsed_time > timeout:
                        logger.error(f"{func.__name__} [{protocol}] timed out after {elapsed_time:.2f}s.")
                        break

                    logger.warning(f"{func.__name__} [{protocol}] failed: {e}. Retrying in {_delay}s...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff

            # Final attempt
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.error(f"{func.__name__} [{protocol}] failed after {tries} attempts: {e}")
                if on_failure:
                    on_failure(e)
                return None
        return wrapper
    return decorator