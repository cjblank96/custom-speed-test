import iperf3
import threading
import statistics
import socket
import time
from config.settings import DOWNLOAD_URLS, FILE_SIZES, PROTOCOL
from utils.logger import logger

PING_ATTEMPTS = 3  # Number of pings per server

def safe_format(value, precision=2, suffix="ms"):
    """Safely format numerical values; return 'N/A' if None."""
    return f"{value:.{precision}f} {suffix}" if value is not None else "N/A"

def ping_server(host):
    """Ping a server to measure latency."""
    latencies = []
    for _ in range(PING_ATTEMPTS):
        try:
            start = time.time()
            sock = socket.create_connection((host, 5201), timeout=2)
            sock.close()
            latency = (time.time() - start) * 1000  # ms
            latencies.append(latency)
        except Exception:
            latencies.append(None)
    successful_pings = [l for l in latencies if l is not None]
    return statistics.mean(successful_pings) if successful_pings else float('inf')

def select_best_download_server():
    """Select the download server with the lowest latency."""
    best_server = None
    lowest_latency = float('inf')

    print("🔍 Testing download servers for the best connection...")
    for server in DOWNLOAD_URLS:
        latency = ping_server(server['host'])
        if latency != float('inf'):
            print(f"✅ {server['host']} - {safe_format(latency)}")
        else:
            print(f"❌ {server['host']} - Unreachable")

        if latency < lowest_latency:
            lowest_latency = latency
            best_server = server

    if best_server:
        print(f"\n🚀 Selected Download Server: {best_server['host']} with {safe_format(lowest_latency)} latency.")
        return best_server
    else:
        logger.error("⚠️ No download servers are reachable.")
        return None

def run_iperf_download_test(server, protocol="tcp"):
    """Run iPerf3 download test against the selected server."""
    client = iperf3.Client()
    client.server_hostname = server['host']
    client.port = server['port']

    if protocol == "udp":
        client.udp = True

    result = client.run()
    if result.error:
        logger.error(f"❌ Download test failed: {result.error}", protocol=protocol)
        return 0
    else:
        speed_mbps = result.received_Mbps
        print(f"📊 Download Speed from {server['host']} over {protocol.upper()}: {safe_format(speed_mbps, suffix='Mbps')}")
        return speed_mbps

def measure_latency_under_load(server, duration=10):
    """Measure latency during active downloads to detect bufferbloat."""
    latencies = []

    def ping_during_download():
        end_time = time.time() + duration
        while time.time() < end_time:
            latency = ping_server(server['host'])
            latencies.append(latency)
            time.sleep(1)

    ping_thread = threading.Thread(target=ping_during_download)
    ping_thread.start()
    return ping_thread, latencies

def download_test(protocol="tcp"):
    """Conducts download speed test using iPerf3 with protocol diversity and latency checks."""
    best_server = select_best_download_server()
    if not best_server:
        logger.error("❌ No server available for download test.", protocol=protocol)
        return 0

    threads, results = [], []

    for file_size in FILE_SIZES:
        logger.info(f"📥 Starting {protocol.upper()} download test for file size {file_size} MB.", protocol=protocol)

        ping_thread, latencies = measure_latency_under_load(best_server)

        t = threading.Thread(target=lambda: results.append(run_iperf_download_test(best_server, protocol=protocol)))
        t.start()
        threads.append(t)

        ping_thread.join()

        if latencies:
            avg_latency = statistics.mean(latencies)
            print(f"📉 Average Latency Under Load: {safe_format(avg_latency)}")
        else:
            logger.warning("⚠️ No latency data collected during load.", protocol=protocol)

    for t in threads:
        t.join()

    if results:
        avg_speed = statistics.mean(results)
        print(f"\n📊 **Average Download Speed ({protocol.upper()}):** {safe_format(avg_speed, suffix='Mbps')}\n")
        return avg_speed
    else:
        logger.error(f"❌ Download test failed for all {protocol.upper()} attempts.", protocol=protocol)
        return 0