def format_speed(bps):
    """Formats speed from bits per second to Mbps or Gbps dynamically."""
    mbps = bps / 1_000_000
    if mbps >= 1000:
        return f"{mbps / 1000:.2f} Gbps"
    return f"{mbps:.2f} Mbps"

def format_size(bytes_size):
    """Formats file size dynamically to KB, MB, GB, or TB."""
    if bytes_size >= 1 << 40:  # 1 TB
        return f"{bytes_size / (1 << 40):.2f} TB"
    elif bytes_size >= 1 << 30:  # 1 GB
        return f"{bytes_size / (1 << 30):.2f} GB"
    elif bytes_size >= 1 << 20:  # 1 MB
        return f"{bytes_size / (1 << 20):.2f} MB"
    elif bytes_size >= 1 << 10:  # 1 KB
        return f"{bytes_size / (1 << 10):.2f} KB"
    return f"{bytes_size} B"

def format_latency(ms):
    """Formats latency in milliseconds with appropriate precision."""
    if ms >= 1000:
        return f"{ms / 1000:.2f} s"
    return f"{ms:.2f} ms"

def format_result_with_protocol(value, protocol="TCP"):
    """Formats result values with protocol context."""
    return f"{value} ({protocol})"