from core.download import download_test
from core.upload import upload_test
from core.latency import latency_test
from utils.logger import logger
from core.visualization import plot_results

if __name__ == "__main__":
    logger.info("⚡ Starting Robust Internet Speed Test with Protocol Diversity...\n")

    # Run Latency Tests for TCP, UDP, ICMP
    latency_results = latency_test()
    
    # Run Download Tests for TCP and UDP
    logger.info("🔽 Starting Download Tests...\n")
    download_tcp = download_test(protocol="tcp")
    download_udp = download_test(protocol="udp")

    # Run Upload Tests for TCP and UDP
    logger.info("🔼 Starting Upload Tests...\n")
    upload_tcp = upload_test(protocol="tcp")
    upload_udp = upload_test(protocol="udp")

    # Collect all results
    results = {
        "download_tcp": download_tcp,
        "download_udp": download_udp,
        "upload_tcp": upload_tcp,
        "upload_udp": upload_udp,
        "latency_tcp": latency_results.get("latency_tcp"),
        "latency_udp": latency_results.get("latency_udp"),
        "latency_icmp": latency_results.get("latency_icmp"),
        "jitter_tcp": latency_results.get("jitter_tcp"),
        "jitter_udp": latency_results.get("jitter_udp"),
        "jitter_icmp": latency_results.get("jitter_icmp"),
        "packet_loss_tcp": latency_results.get("packet_loss_tcp"),
        "packet_loss_udp": latency_results.get("packet_loss_udp"),
        "packet_loss_icmp": latency_results.get("packet_loss_icmp"),
        "latency_under_load": latency_results.get("latency_under_load"),
    }

    # Log Results
    logger.info(f"📡 Latency (TCP): {results['latency_tcp']:.2f} ms, "
                f"(UDP): {results['latency_udp']:.2f} ms, "
                f"(ICMP): {results['latency_icmp']:.2f} ms")

    logger.info(f"📶 Jitter (TCP): {results['jitter_tcp']:.2f} ms, "
                f"(UDP): {results['jitter_udp']:.2f} ms, "
                f"(ICMP): {results['jitter_icmp']:.2f} ms")

    logger.info(f"❌ Packet Loss (TCP): {results['packet_loss_tcp']:.2f}%, "
                f"(UDP): {results['packet_loss_udp']:.2f}%, "
                f"(ICMP): {results['packet_loss_icmp']:.2f}%")

    logger.info(f"🌐 Download Speeds: TCP: {download_tcp:.2f} Mbps, UDP: {download_udp:.2f} Mbps")
    logger.info(f"🚀 Upload Speeds: TCP: {upload_tcp:.2f} Mbps, UDP: {upload_udp:.2f} Mbps")

    # Visualize Results
    plot_results(results)