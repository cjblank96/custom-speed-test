import unittest
from core.latency import latency_test

class TestLatency(unittest.TestCase):
    def test_latency_with_connection(self):
        """Tests latency measurements under normal conditions."""
        latency, jitter, packet_loss = latency_test()

        # Check that latency and jitter are valid numbers or None
        self.assertTrue(latency is None or latency >= 0, "Latency should be non-negative or None")
        self.assertTrue(jitter is None or jitter >= 0, "Jitter should be non-negative or None")
        self.assertTrue(0 <= packet_loss <= 100, "Packet loss must be between 0 and 100")

    def test_latency_with_invalid_host(self):
        """Tests behavior when an invalid hostname is used."""
        from config.settings import LATENCY_TEST_HOST
        LATENCY_TEST_HOST = "invalid.hostname"

        latency, jitter, packet_loss = latency_test()
        self.assertIsNone(latency, "Latency should be None for invalid host")
        self.assertEqual(packet_loss, 100, "Packet loss should be 100% for invalid host")

if __name__ == "__main__":
    unittest.main()
