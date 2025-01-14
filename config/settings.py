# Configuration file for URLs and settings

# Example Download URLs (replace with actual servers)
DOWNLOAD_URLS = [
    "https://speedtest.server1.com",
    "https://speedtest.server2.com",
    "https://speedtest.server3.com"
]


# Upload servers (replace with actual URLs)
UPLOAD_SERVERS = [
    "https://upload-server1.com/upload",
    "https://upload-server2.com/upload"
]

# File sizes in MB for testing
FILE_SIZES = [1, 10, 25, 100]

# Latency test servers
LATENCY_TEST_HOSTS = [
    "google.com",
    "cloudflare.com",
    "amazon.com"
]

# Number of ping attempts
LATENCY_ATTEMPTS = 5

# Protocol selection: 'http1' or 'http3'
PROTOCOL = "http1"
