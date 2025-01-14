import requests
import threading
import statistics
import httpx
from config.settings import DOWNLOAD_URLS
from utils.logger import logger
from utils.retry import retry

@retry((requests.exceptions.RequestException, httpx.HTTPError), tries=3)
def download_file(url, protocol="http1"):
    """
    Downloads a file with automatic retries for transient errors.

    Args:
        url: URL to download from
        protocol: 'http1' or 'http3'

    Returns:
        Download speed in bits per second or 0 on failure
    """
    total_bytes = 0
    start_time = time.time()

    try:
        if protocol == "http3":
            with httpx.Client(http_versions=["h3"]) as client:
                response = client.get(url)
                total_bytes = len(response.content)
        else:
            with requests.get(url, stream=True, timeout=10) as response:
                for chunk in response.iter_content(1024 * 1024):
                    total_bytes += len(chunk)
    except Exception as e:
        logger.error(f"Download failed for {url}: {e}")
        return 0

    elapsed = time.time() - start_time
    return (total_bytes * 8) / elapsed if elapsed > 0 else 0

def download_test(protocol="http1"):
    """
    Executes multi-threaded download speed tests with retries.

    Args:
        protocol: 'http1' or 'http3'

    Returns:
        Average download speed in bits per second
    """
    threads, results = [], []

    for url in DOWNLOAD_URLS:
        t = threading.Thread(target=lambda: results.append(download_file(url, protocol)))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        return statistics.mean(results)
    else:
        logger.error("❌ Download test failed for all URLs.")
        return 0
