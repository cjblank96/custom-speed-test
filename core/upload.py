import requests
import random
import string
import time
from config.settings import UPLOAD_SERVER
from utils.logger import logger
from utils.retry import retry

@retry((requests.exceptions.RequestException,), tries=3)
def upload_file(data):
    """
    Uploads data to the server with retries.

    Args:
        data: Binary data to upload

    Returns:
        Upload speed in bits per second or 0 on failure
    """
    start_time = time.time()
    try:
        response = requests.post(UPLOAD_SERVER, data=data, timeout=15)
        if response.status_code == 200:
            elapsed = time.time() - start_time
            return (len(data) * 8) / elapsed if elapsed > 0 else 0
        else:
            logger.warning(f"Upload failed with status code {response.status_code}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
    return 0

def upload_test():
    """
    Conducts an upload speed test with fault tolerance.

    Returns:
        Upload speed in bits per second
    """
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=10 * 1024 * 1024)).encode('utf-8')
    speed = upload_file(data)

    if speed == 0:
        logger.error("❌ Upload test failed.")
    return speed
