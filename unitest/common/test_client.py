import unittest

from exporter.public.client import StdoutClient, HTTPClient


class TestClient(unittest.TestCase):
    def test_client(self):
        assert True

    def test_stdout_client(self):
        stdout_client = StdoutClient("./empty_file_for_test")
        self.assertEqual(stdout_client.path(), "./empty_file_for_test")
        self.assertEqual(stdout_client.stop(), False)
        self.assertEqual(stdout_client.upload_data(""), False)

    def test_httpclient(self):
        http_client = HTTPClient()
        self.assertEqual(http_client.path(), "localhost:5678")
        self.assertEqual(http_client.stop(), False)
        self.assertEqual(http_client.upload_data(""), True)
