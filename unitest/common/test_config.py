import unittest

from exporter.common.attribute import anyrobot_attribute_from_key_value, anyrobot_attributes_from_key_values, \
    standardize_value_type
from exporter.config.config import Option, Config, Compression
from exporter.public.public import WithCompression


class TestConfig(unittest.TestCase):
    def test_option(self):
        self.assertIsNotNone(WithCompression(Compression(1)).apply(Config()))

    def test_config_equal(self):
        self.assertEqual(Config.__eq__(Config(), ""), False)


if __name__ == "__main__":
    unittest.main()
