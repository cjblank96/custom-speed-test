
# 🌐 Robust Internet Speed Test Tool

This is a professional-grade, feature-rich Internet speed testing tool designed for accurate measurement and analysis of network performance. It uses custom download, upload, and latency testing methods to bypass ISP throttling tactics and offers deep insights into your network.

---

## 🚀 Features

- **Download & Upload Speed Testing** (HTTP/1.1 & HTTP/3)  
- **Latency, Jitter, and Packet Loss Analysis**  
- **Multithreaded Execution** for accurate load simulation  
- **Retry Mechanism** to handle transient network issues  
- **Error Logging** with detailed console and file logs  
- **Results Saved in JSON** for data analysis  
- **Unit Tests** for reliability and future-proofing  

---

## 📂 Project Structure

```
internet-speed-test/
├── main.py                  # Entry point to run the full speed test
├── config/                  # Configuration settings (URLs, hosts, etc.)
├── core/                    # Core modules for download, upload, latency
├── utils/                   # Helper modules for logging, retries, JSON
├── tests/                   # Unit tests for validating components
├── logs/                    # Stores log files of test runs
└── results/                 # Stores JSON-formatted test results
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

Modify `config/settings.py` to adjust test parameters:

```python
DOWNLOAD_URLS = [
    "http://speed.cloudflare.com/__down?bytes=100000000",
    "http://example.com/testfile"
]

UPLOAD_SERVER = "http://your-upload-endpoint.com/upload"
LATENCY_TEST_HOST = "1.1.1.1"
LATENCY_ATTEMPTS = 10
```

---

## 📊 Output

**Console Output Example:**

```
⚡ Starting Robust Internet Speed Test...

📡 Latency: 18.45 ms, 📶 Jitter: 2.13 ms, ❌ Packet Loss: 0.00%
🌐 Download (HTTP/1.1): 93.25 Mbps
🚀 Upload: 35.75 Mbps
✅ Results saved to results/speedtest_results_2025-01-09_14-32-01.json
```

**JSON Output Example (`results/speedtest_results_<timestamp>.json`):**

```json
{
  "timestamp": "2025-01-09 14:32:01",
  "latency_ms": 18.45,
  "jitter_ms": 2.13,
  "packet_loss_percent": 0.0,
  "download_speed_mbps": 93.25,
  "upload_speed_mbps": 35.75
}
```

---

## ✅ Testing

Run the unit tests:

```bash
python -m unittest discover -s tests
```

---

## ❗ Error Handling

- **Automatic Retry:** Handles network issues with exponential backoff.  
- **Detailed Logs:** Errors and warnings are logged to `logs/speedtest.log`.  
- **Graceful Failure:** If one test fails, others continue running.  

---

## 🤝 Contributions

1. Fork the repository.  
2. Create your feature branch (`git checkout -b feature/YourFeature`).  
3. Commit your changes (`git commit -m 'Add feature'`).  
4. Push to the branch (`git push origin feature/YourFeature`).  
5. Open a Pull Request.  

---

## 📜 License

This project is licensed under the MIT License.

---

## 🛠️ Future Features

- Asynchronous download/upload for better performance  
- Advanced analytics and reporting  
- GUI interface for easier operation  

---

## 🔗 Contact

**Your Name**  
📧 your.email@example.com  
🌐 [yourwebsite.com](https://yourwebsite.com)  
