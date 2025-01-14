import socket
import time
import statistics
import subprocess
import threading
from config.settings import LATENCY_TEST_HOSTS, LATENCY_ATTEMPTS
from utils.logger import logger

PING_ATTEMPTS = LATENCY_ATTEMPTS

def safe_format(value, precision=2, suffix="ms"):
    """Safely format numerical values; return 'N/A' if None."""
    return f"{value:.{precision}f} {suffix}" if value is not None else "N/A"

def tcp_ping(host, port=80):
    """Ping a server over TCP."""
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        return (time.time() - start) * 1000  # ms
    except Exception:
        return None

def udp_ping(host, port=33434):
    """Ping a server over UDP using traceroute-like behavior."""
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b'', (host, port))
        sock.recvfrom(512)
        sock.close()
        return (time.time() - start) * 1000  # ms
    except Exception:
        return None

def icmp_ping(host):
    """Ping a server using ICMP."""
    try:
        output = subprocess.run(["ping", "-c", "1", host],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if output.returncode == 0:
            latency_line = [line for line in output.stdout.split("\n") if "time=" in line]
            if latency_line:
                latency = float(latency_line[0].split("time=")[-1].split(" ")[0])
                return latency
        return None
    except Exception:
        return None

def measure_latency_under_load(host, protocol, duration=10):
    """Measure latency during load to detect bufferbloat."""
    latencies = []

    def ping_during_load():
        end_time = time.time() + duration
        while time.time() < end_time:
            if protocol == "tcp":
                latency = tcp_ping(host)
            elif protocol == "udp":
                latency = udp_ping(host)
            else:
                latency = icmp_ping(host)
            if latency is not None:
                latencies.append(latency)
            time.sleep(1)

    ping_thread = threading.Thread(target=ping_during_load)
    ping_thread.start()
    return ping_thread, latencies

def latency_test():
    """Measures latency, jitter, and packet loss across multiple servers with protocol diversity."""
    results = {}

    for host in LATENCY_TEST_HOSTS:
        protocols = ["tcp", "udp", "icmp"]
        for protocol in protocols:
            latencies = []
            for attempt in range(PING_ATTEMPTS):
                if protocol == "tcp":
                    latency = tcp_ping(host)
                elif protocol == "udp":
                    latency = udp_ping(host)
                else:
                    latency = icmp_ping(host)

                if latency is not None:
                    latencies.append(latency)
                    logger.debug(f"{protocol.upper()} Ping {attempt + 1} to {host}: {latency:.2f} ms")
                else:
                    logger.warning(f"{protocol.upper()} Ping {attempt + 1} to {host} failed.")
                time.sleep(0.1)

            successful_pings = [l for l in latencies if l is not None]
            packet_loss = ((PING_ATTEMPTS - len(successful_pings)) / PING_ATTEMPTS) * 100
            avg_latency = statistics.mean(successful_pings) if successful_pings else None
            jitter = statistics.stdev(successful_pings) if len(successful_pings) > 1 else None

            results[f"{host}_{protocol}"] = {
                "avg_latency": avg_latency,
                "jitter": jitter,
                "packet_loss": packet_loss
            }

            print(f"\n📡 **{host} ({protocol.upper()})**\n"
                  f"  - Avg Latency: {safe_format(avg_latency)}\n"
                  f"  - Jitter: {safe_format(jitter)}\n"
                  f"  - Packet Loss: {safe_format(packet_loss, suffix='%')}\n")

    return results