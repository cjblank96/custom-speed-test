def format_speed(bps):
    """Formats speed in bits per second to Mbps for readability."""
    return f"{bps / 1_000_000:.2f} Mbps"
