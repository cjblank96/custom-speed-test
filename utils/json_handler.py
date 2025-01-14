import json
import os
from datetime import datetime
from utils.logger import logger

def save_results(results, filename=None):
    """
    Saves the results to a JSON file with error handling.

    Args:
        results: Dictionary of speed test results
        filename: Custom filename (auto-generated if None)
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"results/speedtest_results_{timestamp}.json"

    try:
        os.makedirs("results", exist_ok=True)  # Ensure results directory exists
    except Exception as e:
        logger.error(f"Failed to create results directory: {e}")
        return

    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"✅ Results saved to {filename}")
    except PermissionError:
        logger.error(f"❌ Permission denied when saving results to {filename}")
    except TypeError as e:
        logger.error(f"❌ Failed to serialize results: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error while saving results: {e}")

def load_results(filename):
    """
    Loads results from a JSON file with error handling.

    Args:
        filename: Path to the JSON file

    Returns:
        Dictionary of results or None on failure
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            logger.info(f"✅ Results loaded from {filename}")
            return data
    except FileNotFoundError:
        logger.error(f"❌ File not found: {filename}")
    except json.JSONDecodeError:
        logger.error(f"❌ JSON is malformed in file: {filename}")
    except Exception as e:
        logger.error(f"❌ Unexpected error while loading results: {e}")
    return None
