import matplotlib.pyplot as plt

def plot_results(results):
    """Generates a bar chart of the speed test results."""
    
    labels = ["Download (HTTP/1.1)", "Download (HTTP/3)", "Upload", "Latency", "Jitter"]
    values = [
        results["download_http1"],
        results["download_http3"],
        results["upload"],
        results["latency"],
        results["jitter"]
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'cyan', 'green', 'orange', 'red'])
    plt.ylabel("Speed (Mbps) / Time (ms)")
    plt.title("Internet Speed Test Results")
    plt.show()
