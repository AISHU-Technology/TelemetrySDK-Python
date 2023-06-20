import unittest

from exporter.public.client import StdoutClient, HTTPClient, ConsoleClient, FileClient


class TestClient(unittest.TestCase):
    def test_client(self):
        assert True

    def test_console_client(self):
        console_client = ConsoleClient()
        self.assertEqual(console_client.path(), "Console")
        self.assertEqual(console_client.stop(), False)
        self.assertEqual(console_client.upload_data(""), False)

    def test_file_client(self):
        file_client = FileClient("./empty_file_for_test")
        self.assertEqual(file_client.path(), "./empty_file_for_test")
        self.assertEqual(file_client.stop(), False)
        self.assertEqual(file_client.upload_data(""), False)

    def test_stdout_client(self):
        stdout_client = StdoutClient("./empty_file_for_test")
        self.assertEqual(stdout_client.path(), "./empty_file_for_test")
        self.assertEqual(stdout_client.stop(), False)
        self.assertEqual(stdout_client.upload_data(""), False)

    def test_httpclient(self):
        http_client = HTTPClient()
        self.assertEqual(http_client.path(), "localhost:5678")
        self.assertEqual(http_client.stop(), False)


if __name__ == "__main__":
    unittest.main()
