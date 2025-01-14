import sys

def format_speed(speed_mbps):
    """Dynamically format speed into Mbps or Gbps."""
    if speed_mbps >= 1000:
        return f"{speed_mbps / 1000:.2f} Gbps"
    else:
        return f"{speed_mbps:.2f} Mbps"

def format_size(size_mb):
    """Dynamically format size into MB or GB."""
    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    else:
        return f"{size_mb:.2f} MB"

def progress_bar(task_name, current, total, speed, protocol="TCP", latency=None):
    """Displays a real-time progress bar with protocol and latency under load.

    :param task_name: Task name (Download/Upload/Ping)
    :param current: Current data transferred or progress value
    :param total: Total data to transfer or complete
    :param speed: Current speed in Mbps
    :param protocol: Protocol used (TCP/UDP/HTTP3)
    :param latency: Optional latency under load (ms)
    """
    bar_length = 50
    progress = current / total if total != 0 else 0
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    speed_display = format_speed(speed)
    current_display = format_size(current)
    total_display = format_size(total)
    latency_display = f" | Latency: {latency:.2f} ms" if latency else ""

    sys.stdout.write(
        f"\r{task_name} [{protocol}]: |{bar}| {progress * 100:.2f}% "
        f"{current_display}/{total_display} @ {speed_display}{latency_display}"
    )
    sys.stdout.flush()

    if current >= total:
        print(f"\n✅ {task_name} [{protocol}] Completed!\n")