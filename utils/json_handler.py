import json
import os
import gzip
from datetime import datetime
from utils.logger import logger

def validate_results(results):
    """Validates the structure of the results dictionary."""
    required_keys = ["download_tcp", "download_udp", "upload_tcp", "upload_udp",
                     "latency_tcp", "latency_udp", "latency_icmp",
                     "jitter_tcp", "jitter_udp", "jitter_icmp",
                     "packet_loss_tcp", "packet_loss_udp", "packet_loss_icmp"]

    for key in required_keys:
        if key not in results:
            logger.error(f"❌ Missing required key in results: {key}")
            return False
    return True

def save_results(results, filename=None, compress=False):
    """Saves the results to a JSON file with protocol tagging and optional compression.

    Args:
        results: Dictionary of speed test results
        filename: Custom filename (auto-generated if None)
        compress: Whether to compress the results file (gzip)
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"results/speedtest_results_{timestamp}.json"

    if compress:
        filename += ".gz"

    if not validate_results(results):
        logger.error("❌ Results failed validation. Not saving.")
        return

    try:
        os.makedirs("results", exist_ok=True)  # Ensure results directory exists
    except Exception as e:
        logger.error(f"❌ Failed to create results directory: {e}")
        return

    try:
        if compress:
            with gzip.open(filename, 'wt', encoding='utf-8') as f:
                json.dump(results, f, indent=4)
        else:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
        logger.info(f"✅ Results saved to {filename}")
    except (PermissionError, TypeError, Exception) as e:
        logger.error(f"❌ Failed to save results: {e}")

def load_results(filename):
    """Loads results from a JSON or compressed JSON file with validation.

    Args:
        filename: Path to the JSON file

    Returns:
        Dictionary of results or None on failure
    """
    try:
        if filename.endswith('.gz'):
            with gzip.open(filename, 'rt', encoding='utf-8') as f:
                data = json.load(f)
        else:
            with open(filename, 'r') as f:
                data = json.load(f)

        if validate_results(data):
            logger.info(f"✅ Results loaded from {filename}")
            return data
        else:
            logger.error(f"❌ Invalid data structure in {filename}")
            return None
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        logger.error(f"❌ Failed to load results from {filename}: {e}")
        return None

def merge_results(existing_results, new_results):
    """Merges two results dictionaries by averaging values where possible."""
    merged = {}

    for key in set(existing_results) | set(new_results):
        if key in existing_results and key in new_results:
            merged[key] = (existing_results[key] + new_results[key]) / 2
        elif key in existing_results:
            merged[key] = existing_results[key]
        else:
            merged[key] = new_results[key]

    logger.info("🔄 Results merged successfully.")
    return merged