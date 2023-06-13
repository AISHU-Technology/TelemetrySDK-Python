import unittest

from exporter.version.version import TelemetrySDKVersion


class TestVersion(unittest.TestCase):
    def test_telemetry_sdk_version(self):
        self.assertEqual(TelemetrySDKVersion, "2.4.0")


if __name__ == "__main__":
    unittest.main()
