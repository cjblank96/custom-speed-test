
# 🌐 Advanced Internet Speed Testing Tool

This is a **professional-grade**, feature-rich internet speed testing tool designed for highly accurate measurement and analysis of network performance. By leveraging **iPerf3**, protocol diversity (**TCP**, **UDP**, **HTTP/1.1**, **HTTP/3**), and bufferbloat detection, this tool delivers real-world network performance insights that surpass common testing platforms.

---

## 🚀 Key Features

- **Protocol-Diverse Testing:** Measures download/upload speeds over **TCP**, **UDP**, **HTTP/1.1**, and **HTTP/3**.  
- **Latency, Jitter, and Packet Loss Analysis:** Detailed metrics across multiple protocols.  
- **Bufferbloat Detection:** Measures latency under load to reveal hidden performance issues.  
- **Dynamic Server Selection:** Automatically selects the best server based on latency.  
- **Real-World Data Simulation:** Uses realistic data patterns for uploads/downloads.  
- **Parallel Multi-threaded Testing:** Simulates real-world traffic with simultaneous connections.  
- **Comprehensive Logging:** Color-coded console logs and rotating file logs with protocol context.  
- **Interactive Visualization:** Graphical display of results for speed, latency, jitter, and packet loss.  
- **Robust Error Handling:** Retry logic with timeout controls and custom failure handling.  
- **Compressed Result Storage:** Option to save results in compressed `.json.gz` format.

---

## 📂 Project Structure

```
internet-speed-test/
├── main.py                  # Entry point for full-speed tests
├── config/                  # Settings for servers, protocols, and file sizes
├── core/                    # Core modules: download, upload, latency, visualization
├── utils/                   # Helpers: logger, retry, JSON handling, progress bar
├── tests/                   # Unit tests for validating core functionality
├── logs/                    # Rotating log files
└── results/                 # JSON/GZIP-formatted test results
```

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/internet-speed-test.git
cd internet-speed-test
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the tool**

```bash
python main.py
```

---

## 📝 Configuration

Customize testing parameters in `config/settings.py`:

```python
DOWNLOAD_URLS = [
    "http://den.speedtest.clouvider.net/1GB.bin",  # Denver, CO
    "http://dal.speedtest.clouvider.net/1GB.bin",  # Dallas, TX
]

UPLOAD_SERVERS = [
    {"host": "iperf.he.net", "port": 5201},  # Fremont, CA
    {"host": "iperf3.volia.net", "port": 5201},  # Kyiv, Ukraine
]

LATENCY_TEST_HOSTS = ["8.8.8.8", "1.1.1.1", "13.32.0.0"]

FILE_SIZES = [1, 10, 100, 500, 1024]

PROTOCOL = ["http1", "http3", "tcp", "udp"]
```

---

## 🏃 How It Works

1. **Latency Tests:**  
   Measures latency, jitter, and packet loss across **TCP**, **UDP**, and **ICMP**.

2. **Download & Upload Tests:**  
   Conducts **iPerf3-based** download and upload speed tests over **TCP** and **UDP** with multi-threading.

3. **Latency Under Load:**  
   Detects **bufferbloat** by measuring latency during active downloads/uploads.

4. **Logging & Visualization:**  
   Logs detailed results and generates clear **visual charts** for speed, latency, jitter, and packet loss.

5. **Result Saving:**  
   Saves results in structured **JSON** or compressed **`.json.gz`** formats.

---

## 📊 Example Output

**Console Output:**

```
⚡ Starting Robust Internet Speed Test...

📡 Latency (TCP): 18.45 ms | UDP: 20.13 ms | ICMP: 17.25 ms
📶 Jitter (TCP): 1.23 ms | UDP: 1.55 ms | ICMP: 1.10 ms
❌ Packet Loss (TCP): 0.00% | UDP: 0.50% | ICMP: 0.00%
🌐 Download Speeds: TCP: 935.25 Mbps | UDP: 850.75 Mbps
🚀 Upload Speeds: TCP: 355.75 Mbps | UDP: 340.60 Mbps
📉 Bufferbloat Latency Under Load: 35.22 ms
✅ Results saved to results/speedtest_results_2025-01-14_14-32-01.json.gz
```

**Sample JSON Result:**

```json
{
  "timestamp": "2025-01-14 14:32:01",
  "latency_tcp": 18.45,
  "latency_udp": 20.13,
  "latency_icmp": 17.25,
  "jitter_tcp": 1.23,
  "packet_loss_udp": 0.5,
  "download_tcp": 935.25,
  "download_udp": 850.75,
  "upload_tcp": 355.75,
  "upload_udp": 340.60,
  "latency_under_load": 35.22
}
```

---

## ✅ Running Tests

Run the unit tests to ensure functionality:

```bash
python -m unittest discover -s tests
```

---

## 📜 License

This project is licensed under the MIT License.
