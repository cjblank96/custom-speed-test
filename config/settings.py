# Configuration file for URLs and settings

# Download Servers
DOWNLOAD_URLS = [
    "http://den.speedtest.clouvider.net/1GB.bin",  # Denver, CO
    "http://dal.speedtest.clouvider.net/1GB.bin",  # Dallas, TX
    "http://chi.speedtest.clouvider.net/1GB.bin",  # Chicago, IL
    "http://kc.speedtest.clouvider.net/1GB.bin",   # Kansas City, MO
    "http://stl.speedtest.clouvider.net/1GB.bin",  # St. Louis, MO
    "http://okc.speedtest.clouvider.net/1GB.bin",  # Oklahoma City, OK
    "http://oma.speedtest.clouvider.net/1GB.bin",  # Omaha, NE
    "http://msn.speedtest.clouvider.net/1GB.bin",  # Madison, WI
    "http://ind.speedtest.clouvider.net/1GB.bin",  # Indianapolis, IN
    "http://col.speedtest.clouvider.net/1GB.bin",  # Columbus, OH
    "http://nsh.speedtest.clouvider.net/1GB.bin",  # Nashville, TN
    "http://mem.speedtest.clouvider.net/1GB.bin",  # Memphis, TN
    "http://bna.speedtest.clouvider.net/1GB.bin",  # Birmingham, AL
    "http://lou.speedtest.clouvider.net/1GB.bin",  # Louisville, KY
    "http://cvg.speedtest.clouvider.net/1GB.bin",  # Cincinnati, OH
    "http://cle.speedtest.clouvider.net/1GB.bin",  # Cleveland, OH
    "http://det.speedtest.clouvider.net/1GB.bin",  # Detroit, MI
    "http://msp.speedtest.clouvider.net/1GB.bin",  # Minneapolis, MN
    "http://mil.speedtest.clouvider.net/1GB.bin",  # Milwaukee, WI
    "http://grr.speedtest.clouvider.net/1GB.bin"   # Grand Rapids, MI
]

# Upload Servers (replace with real iPerf3 servers)
UPLOAD_SERVERS = [
    {"host": "iperf.he.net", "port": 5201},           # Fremont, CA (Hurricane Electric)
    {"host": "iperf3.volia.net", "port": 5201},       # Kyiv, Ukraine (Volia)
    {"host": "iperf.scottlinux.com", "port": 5201},   # Chicago, IL
    {"host": "iperf.biznetnetworks.com", "port": 5201},  # Indonesia
    {"host": "iperf.fr", "port": 5201}               # France
]

# File sizes in MB for testing
FILE_SIZES = [1, 10, 25, 100, 500, 1024]  # Added larger files for thorough testing

# Latency test servers (using IPs for consistency)
LATENCY_TEST_HOSTS = [
    "8.8.8.8",   # Google DNS
    "1.1.1.1",   # Cloudflare DNS
    "13.32.0.0"  # Amazon AWS
]

# Number of ping attempts
LATENCY_ATTEMPTS = 5

# Protocol selection: support both 'http1' and 'http3'
PROTOCOL = ["http1", "http3"]