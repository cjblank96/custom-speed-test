from core.download import download_test
from core.upload import upload_test
from core.latency import latency_test
from utils.logger import logger

if __name__ == "__main__":
    logger.info("⚡ Starting Robust Internet Speed Test...\n")

    latency, jitter, packet_loss = latency_test()
    download_http1 = download_test(protocol="http1")
    upload_speed = upload_test()

    logger.info(f"📡 Latency: {latency:.2f} ms, 📶 Jitter: {jitter:.2f} ms, ❌ Packet Loss: {packet_loss:.2f}%")
    logger.info(f"🌐 Download (HTTP/1.1): {download_http1 / 1_000_000:.2f} Mbps")
    logger.info(f"🚀 Upload: {upload_speed / 1_000_000:.2f} Mbps")
