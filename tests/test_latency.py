import unittest
from core.latency import latency_test, measure_latency_under_load
from config.settings import LATENCY_TEST_HOSTS

class TestLatency(unittest.TestCase):
    def test_latency_tcp(self):
        """Tests TCP latency measurement."""
        results = latency_test()
        latency_tcp = results.get("latency_tcp")
        self.assertIsNotNone(latency_tcp, "TCP Latency should not be None")
        self.assertGreaterEqual(latency_tcp, 0, "TCP Latency should be non-negative")

    def test_latency_udp(self):
        """Tests UDP latency measurement."""
        results = latency_test()
        latency_udp = results.get("latency_udp")
        self.assertIsNotNone(latency_udp, "UDP Latency should not be None")
        self.assertGreaterEqual(latency_udp, 0, "UDP Latency should be non-negative")

    def test_latency_icmp(self):
        """Tests ICMP latency measurement."""
        results = latency_test()
        latency_icmp = results.get("latency_icmp")
        self.assertIsNotNone(latency_icmp, "ICMP Latency should not be None")
        self.assertGreaterEqual(latency_icmp, 0, "ICMP Latency should be non-negative")

    def test_latency_under_load(self):
        """Tests latency measurement during load (bufferbloat detection)."""
        host = LATENCY_TEST_HOSTS[0]  # Use the first host for testing
        _, latencies = measure_latency_under_load(host, protocol="tcp", duration=5)
        self.assertTrue(all(l >= 0 for l in latencies), "All latency under load values should be non-negative")

    def test_invalid_host(self):
        """Tests behavior when an invalid hostname is used."""
        invalid_host = "invalid.hostname"
        _, latencies = measure_latency_under_load(invalid_host, protocol="tcp", duration=3)
        self.assertTrue(all(l is None for l in latencies), "Latency should be None for an invalid host")

if __name__ == "__main__":
    unittest.main()