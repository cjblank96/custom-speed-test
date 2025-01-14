import matplotlib.pyplot as plt

def plot_results(results):
    """Generates bar charts for the speed test results across multiple protocols."""

    # Extract download/upload speeds for TCP and UDP
    download_tcp = results.get("download_tcp", 0)
    download_udp = results.get("download_udp", 0)
    upload_tcp = results.get("upload_tcp", 0)
    upload_udp = results.get("upload_udp", 0)

    # Extract latency, jitter, and packet loss for each protocol
    latency_tcp = results.get("latency_tcp", 0)
    latency_udp = results.get("latency_udp", 0)
    latency_icmp = results.get("latency_icmp", 0)
    jitter_tcp = results.get("jitter_tcp", 0)
    jitter_udp = results.get("jitter_udp", 0)
    jitter_icmp = results.get("jitter_icmp", 0)
    packet_loss_tcp = results.get("packet_loss_tcp", 0)
    packet_loss_udp = results.get("packet_loss_udp", 0)
    packet_loss_icmp = results.get("packet_loss_icmp", 0)

    # Latency under load (Bufferbloat)
    latency_under_load = results.get("latency_under_load", 0)

    # Bar chart for Download/Upload Speeds
    labels_speed = ["Download TCP", "Download UDP", "Upload TCP", "Upload UDP"]
    values_speed = [download_tcp, download_udp, upload_tcp, upload_udp]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_speed, values_speed, color=["blue", "cyan", "green", "lightgreen"])
    plt.ylabel("Speed (Mbps)")
    plt.title("Download and Upload Speeds (TCP/UDP)")
    plt.show()

    # Bar chart for Latency across protocols
    labels_latency = ["TCP", "UDP", "ICMP", "Under Load"]
    values_latency = [latency_tcp, latency_udp, latency_icmp, latency_under_load]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_latency, values_latency, color=["orange", "purple", "gray", "red"])
    plt.ylabel("Latency (ms)")
    plt.title("Latency Across Protocols and Under Load")
    plt.show()

    # Bar chart for Jitter across protocols
    labels_jitter = ["TCP", "UDP", "ICMP"]
    values_jitter = [jitter_tcp, jitter_udp, jitter_icmp]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_jitter, values_jitter, color=["yellow", "pink", "brown"])
    plt.ylabel("Jitter (ms)")
    plt.title("Jitter Across Protocols")
    plt.show()

    # Bar chart for Packet Loss across protocols
    labels_packet_loss = ["TCP", "UDP", "ICMP"]
    values_packet_loss = [packet_loss_tcp, packet_loss_udp, packet_loss_icmp]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_packet_loss, values_packet_loss, color=["magenta", "lime", "navy"])
    plt.ylabel("Packet Loss (%)")
    plt.title("Packet Loss Across Protocols")
    plt.show()