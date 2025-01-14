import requests
import threading
import random
import string
import time
import statistics
import socket
from config.settings import UPLOAD_SERVERS, FILE_SIZES, PROTOCOL
from utils.logger import logger
from utils.retry import retry
from utils.progress_bar import progress_bar

PING_ATTEMPTS = 3  # Number of pings for server selection


def ping_server(host):
    """Ping a server to measure latency."""
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


def select_best_upload_server():
    """Select the upload server with the lowest latency."""
    best_server = None
    lowest_latency = float('inf')

    print("🔍 Testing upload servers for the best connection...")
    for url in UPLOAD_SERVERS:
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
        print(f"\n🚀 Selected Upload Server: {best_server} with {lowest_latency:.2f} ms latency.")
        return best_server
    else:
        logger.error("⚠️ No upload servers are reachable.")
        return None


@retry((requests.exceptions.RequestException,), tries=3)
def upload_file(url, data):
    """Uploads data to the server with real-time progress."""
    start_time = time.time()
    total_bytes = 0

    try:
        with requests.post(url, data=data, stream=True, timeout=15) as response:
            if response.status_code == 200:
                total_size = len(data)
                for chunk in data:
                    total_bytes += len(chunk)
                    elapsed = time.time() - start_time
                    speed_mbps = (total_bytes * 8) / (elapsed * 1_000_000)
                    progress_bar("Uploading", total_bytes / 1_000_000, total_size / 1_000_000, speed_mbps)
                elapsed = time.time() - start_time
                return (total_bytes * 8) / elapsed if elapsed > 0 else 0
            else:
                logger.warning(f"Upload failed with status code {response.status_code}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
    return 0


def upload_test():
    """Conducts parallel upload speed tests with real-time progress and server selection."""
    best_server = select_best_upload_server()
    if not best_server:
        logger.error("❌ No server available for upload test.")
        return 0

    threads, results = [], []

    for file_size in FILE_SIZES:
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size * 1024 * 1024)).encode('utf-8')
        t = threading.Thread(target=lambda: results.append(upload_file(best_server, data)))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        avg_speed = statistics.mean(results)
        print(f"\n📊 **Average Upload Speed:** {avg_speed / 1_000_000:.2f} Mbps\n")
        return avg_speed
    else:
        logger.error("❌ Upload test failed for all file sizes.")
        return 0