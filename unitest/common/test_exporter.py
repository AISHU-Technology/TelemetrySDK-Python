import unittest

from exporter.public.client import StdoutClient
from exporter.public.exporter import Exporter


class TestExporter(unittest.TestCase):
    def test_name(self):
        exporter = Exporter(StdoutClient())
        self.assertEqual(exporter.name, "./AnyRobotData.json")

    def test_shutdown(self):
        exporter = Exporter(StdoutClient())
        self.assertEqual(exporter.shutdown(), False)

    def test_export_data(self):
        exporter = Exporter(StdoutClient())
        self.assertEqual(exporter.export_data(""), False)

    def test_client(self):
        exporter = Exporter(StdoutClient())
        self.assertEqual(exporter.client, exporter.client)


if __name__ == "__main__":
    unittest.main()
