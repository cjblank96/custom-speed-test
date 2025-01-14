import requests
import threading
import statistics
import httpx
import time
import socket
from config.settings import DOWNLOAD_URLS, FILE_SIZES, PROTOCOL
from utils.logger import logger
from utils.retry import retry
from utils.progress_bar import progress_bar

PING_ATTEMPTS = 3  # Number of pings per server


def ping_server(host):
    """
    Ping a server to measure latency.

    Args:
        host (str): Hostname of the server.

    Returns:
        float: Average latency in milliseconds.
    """
    latencies = []
    for _ in range(PING_ATTEMPTS):
        try:
            start = time.time()
            sock = socket.create_connection((host, 80), timeout=2)
            sock.close()
            latency = (time.time() - start) * 1000  # ms
            latencies.append(latency)
        except Exception:
            latencies.append(None)
    successful_pings = [l for l in latencies if l is not None]
    return statistics.mean(successful_pings) if successful_pings else float('inf')


def select_best_server():
    """
    Select the server with the lowest latency.

    Returns:
        str: The URL of the fastest server.
    """
    best_server = None
    lowest_latency = float('inf')

    print("🔍 Testing servers for the best connection...")
    for url in DOWNLOAD_URLS:
        host = url.replace("https://", "").replace("http://", "").split('/')[0]
        latency = ping_server(host)
        if latency != float('inf'):
            print(f"✅ {host} - {latency:.2f} ms")
        else:
            print(f"❌ {host} - Unreachable")

        if latency < lowest_latency:
            lowest_latency = latency
            best_server = url

    if best_server:
        print(f"\n🚀 Selected Server: {best_server} with {lowest_latency:.2f} ms latency.")
        return best_server
    else:
        logger.error("⚠️ No servers are reachable.")
        return None


@retry((requests.exceptions.RequestException, httpx.HTTPError), tries=3)
def download_file(url, protocol="http1", file_size=10):
    """
    Download a file from a server with real-time progress display.

    Args:
        url (str): URL of the download server.
        protocol (str): 'http1' or 'http3'.
        file_size (int): Size of the file in MB.

    Returns:
        float: Download speed in bits per second.
    """
    total_bytes = 0
    start_time = time.time()
    download_url = f"{url}/{file_size}MB"

    try:
        if protocol == "http3":
            with httpx.Client(http_versions=["h3"]) as client:
                response = client.get(download_url)
                total_bytes = len(response.content)
        else:
            with requests.get(download_url, stream=True, timeout=10) as response:
                total_size = int(response.headers.get('content-length', 0))
                for chunk in response.iter_content(1024 * 1024):
                    total_bytes += len(chunk)
                    elapsed = time.time() - start_time
                    speed_mbps = (total_bytes * 8) / (elapsed * 1_000_000)
                    progress_bar("Downloading", total_bytes / 1_000_000, total_size / 1_000_000, speed_mbps)
    except Exception as e:
        logger.error(f"Download failed for {download_url}: {e}")
        return 0

    elapsed = time.time() - start_time
    return (total_bytes * 8) / elapsed if elapsed > 0 else 0


def download_test():
    """
    Conduct multi-threaded download speed tests with real-time progress and automatic server selection.

    Returns:
        float: Average download speed in bits per second.
    """
    best_server = select_best_server()
    if not best_server:
        logger.error("❌ No server available for download test.")
        return 0

    threads, results = [], []

    for file_size in FILE_SIZES:
        t = threading.Thread(target=lambda: results.append(download_file(best_server, PROTOCOL, file_size)))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        avg_speed = statistics.mean(results)
        print(f"\n📊 **Average Download Speed:** {avg_speed / 1_000_000:.2f} Mbps\n")
        return avg_speed
    else:
        logger.error("❌ Download test failed for all file sizes.")
        return 0