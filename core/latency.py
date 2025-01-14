import socket
import time
import statistics
from config.settings import LATENCY_TEST_HOST, LATENCY_ATTEMPTS
from utils.logger import logger
from utils.retry import retry

@retry((socket.timeout, socket.gaierror), tries=3)
def ping(host):
    """Performs a single ping."""
    start = time.time()
    sock = socket.create_connection((host, 80), timeout=2)
    sock.close()
    return (time.time() - start) * 1000

def latency_test():
    """
    Measures latency, jitter, and packet loss with retries.
    
    Returns:
        avg_latency: Average latency in ms
        jitter: Jitter in ms
        packet_loss: Packet loss in %
    """
    latencies = []

    for attempt in range(LATENCY_ATTEMPTS):
        try:
            latency = ping(LATENCY_TEST_HOST)
            latencies.append(latency)
            logger.debug(f"Ping {attempt + 1}: {latency:.2f} ms")
        except Exception as e:
            logger.warning(f"Ping {attempt + 1} failed: {e}")
            latencies.append(None)
        time.sleep(0.1)

    successful_pings = [l for l in latencies if l is not None]
    packet_loss = ((LATENCY_ATTEMPTS - len(successful_pings)) / LATENCY_ATTEMPTS) * 100

    avg_latency = statistics.mean(successful_pings) if successful_pings else None
    jitter = statistics.stdev(successful_pings) if len(successful_pings) > 1 else None

    return avg_latency, jitter, packet_loss
