import iperf3
import threading
import statistics
import socket
import random
import string
import time
from config.settings import UPLOAD_SERVERS, FILE_SIZES, PROTOCOL
from utils.logger import logger

PING_ATTEMPTS = 3  # Number of pings for server selection

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

def select_best_upload_server():
    """Select the upload server with the lowest latency."""
    best_server = None
    lowest_latency = float('inf')

    print("🔍 Testing upload servers for the best connection...")
    for server in UPLOAD_SERVERS:
        latency = ping_server(server['host'])
        if latency != float('inf'):
            print(f"✅ {server['host']} - {latency:.2f} ms")
        else:
            print(f"❌ {server['host']} - Unreachable")

        if latency < lowest_latency:
            lowest_latency = latency
            best_server = server

    if best_server:
        print(f"\n🚀 Selected Upload Server: {best_server['host']} with {lowest_latency:.2f} ms latency.")
        return best_server
    else:
        logger.error("⚠️ No upload servers are reachable.")
        return None

def run_iperf_upload_test(server, protocol="tcp"):
    """Run iPerf3 upload test against the selected server with TCP/UDP."""
    client = iperf3.Client()
    client.server_hostname = server['host']
    client.port = server['port']
    client.reverse = True  # Upload test

    if protocol == "udp":
        client.udp = True

    result = client.run()
    if result.error:
        logger.error(f"❌ Upload test failed: {result.error}")
        return 0
    else:
        speed_mbps = result.sent_Mbps
        print(f"📊 Upload Speed to {server['host']} over {protocol.upper()}: {speed_mbps:.2f} Mbps")
        return speed_mbps

def generate_realistic_data(size_mb):
    """Simulate real-world file uploads with mixed data types."""
    types = [string.ascii_letters, string.digits, '!@#$%^&*()_+']
    data = ''.join(random.choices(''.join(types), k=size_mb * 1024 * 1024)).encode('utf-8')
    return data

def measure_latency_under_load(server, duration=10):
    """Measure latency during an active upload to detect bufferbloat."""
    latencies = []

    def ping_during_upload():
        end_time = time.time() + duration
        while time.time() < end_time:
            latency = ping_server(server['host'])
            latencies.append(latency)
            time.sleep(1)

    ping_thread = threading.Thread(target=ping_during_upload)
    ping_thread.start()
    return ping_thread, latencies

def upload_test():
    """Conducts upload speed test with iPerf3 and measures latency under load."""
    best_server = select_best_upload_server()
    if not best_server:
        logger.error("❌ No server available for upload test.")
        return 0

    threads, results = [], []

    for protocol in ["tcp", "udp"]:
        for file_size in FILE_SIZES:
            data = generate_realistic_data(file_size)
            ping_thread, latencies = measure_latency_under_load(best_server)

            t = threading.Thread(target=lambda: results.append(run_iperf_upload_test(best_server, protocol=protocol)))
            t.start()
            threads.append(t)

            ping_thread.join()

            print(f"📉 Average Latency Under Load: {statistics.mean(latencies):.2f} ms")

    for t in threads:
        t.join()

    if results:
        avg_speed = statistics.mean(results)
        print(f"\n📊 **Average Upload Speed:** {avg_speed:.2f} Mbps\n")
        return avg_speed
    else:
        logger.error("❌ Upload test failed for all attempts.")
        return 0