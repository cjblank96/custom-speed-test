import socket
import time
import statistics
from config.settings import LATENCY_TEST_HOSTS, LATENCY_ATTEMPTS
from utils.logger import logger
from utils.retry import retry


@retry((socket.timeout, socket.gaierror), tries=3)
def ping(host):
    """Performs a single ping."""
    start = time.time()
    try:
        sock = socket.create_connection((host, 80), timeout=2)
        sock.close()
        return (time.time() - start) * 1000  # Convert to milliseconds
    except Exception:
        return None


def latency_test():
    """Measures latency, jitter, and packet loss across multiple servers."""
    results = {}

    for host in LATENCY_TEST_HOSTS:
        latencies = []
        for attempt in range(LATENCY_ATTEMPTS):
            latency = ping(host)
            if latency is not None:
                latencies.append(latency)
                logger.debug(f"Ping {attempt + 1} to {host}: {latency:.2f} ms")
            else:
                logger.warning(f"Ping {attempt + 1} to {host} failed.")
            time.sleep(0.1)

        successful_pings = [l for l in latencies if l is not None]
        packet_loss = ((LATENCY_ATTEMPTS - len(successful_pings)) / LATENCY_ATTEMPTS) * 100
        avg_latency = statistics.mean(successful_pings) if successful_pings else None
        jitter = statistics.stdev(successful_pings) if len(successful_pings) > 1 else None

        results[host] = {
            "avg_latency": avg_latency,
            "jitter": jitter,
            "packet_loss": packet_loss
        }

        print(f"\n📡 **{host}**\n"
              f"  - Avg Latency: {avg_latency:.2f} ms\n"
              f"  - Jitter: {jitter:.2f} ms\n"
              f"  - Packet Loss: {packet_loss:.2f}%\n")

    return results