import unittest

from exporter.config.config import Config, Compression
from exporter.public.public import (
    WithAnyRobotURL,
    WithCompression,
    WithTimeout,
    WithHeader,
    WithRetry,
)


class TestPublic(unittest.TestCase):
    def test_with_any_robot_url(self):
        cfg = Config()
        url = "a.b.c.d"
        cfg.endpoint = url
        self.assertNotEqual(WithAnyRobotURL(url).apply(Config()), cfg)

        url = "https://a.b.c.d/api"
        cfg.endpoint = url
        self.assertEqual(WithAnyRobotURL(url).apply(Config()), cfg)

    def test_with_compression(self):
        cfg = Config()
        compression = 3
        cfg.compression = compression
        self.assertNotEqual(WithCompression(compression).apply(Config()), cfg)

        cfg = Config()
        compression = Compression.NoCompression
        cfg.compression = compression
        self.assertEqual(WithCompression(compression).apply(Config()), cfg)

    def test_with_timeout(self):
        cfg = Config()
        timeout = 1200
        cfg.timeout = timeout
        self.assertNotEqual(WithTimeout(timeout).apply(Config()), cfg)

        cfg = Config()
        timeout = 12
        cfg.timeout = timeout
        self.assertEqual(WithTimeout(timeout).apply(Config()), cfg)

    def test_with_header(self):
        cfg = Config()
        headers = {"test": "test"}
        cfg.headers = headers
        self.assertEqual(WithHeader(headers).apply(Config()), cfg)

    def test_with_retry(self):
        cfg = Config()
        retry = -1.3
        cfg.max_elapsed_time = retry
        self.assertNotEqual(WithRetry(retry).apply(Config()), cfg)

        cfg = Config()
        retry = 12
        cfg.max_elapsed_time = retry
        self.assertEqual(WithRetry(retry).apply(Config()), cfg)


if __name__ == "__main__":
    unittest.main()
