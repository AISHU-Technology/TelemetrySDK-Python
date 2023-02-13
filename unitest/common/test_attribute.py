import unittest

from exporter.common.attribute import anyrobot_attribute_from_key_value, anyrobot_attributes_from_key_values, \
    standardize_value_type


class TestAttribute(unittest.TestCase):
    def test_anyrobot_resource_from_resource(self):
        assert True

    def test_anyrobot_attributes_from_key_values(self):
        key_values = {"name": "Rocky"}
        self.assertEqual(anyrobot_attributes_from_key_values(key_values),
                         '[{"Key": "name", "Value": {"Type": "STRING", "Value": "Rocky"}}]')

    def test_anyrobot_attribute_from_key_value(self):
        self.assertEqual(anyrobot_attribute_from_key_value("name", "Rocky"),
                         '{"Key": "name", "Value": {"Type": "STRING", "Value": "Rocky"}}')

    def test_standardize_value_type(self):
        self.assertEqual(standardize_value_type(True), "BOOL")
        self.assertEqual(standardize_value_type(12), "INT")
        self.assertEqual(standardize_value_type(3.4), "FLOAT")
        self.assertEqual(standardize_value_type(""), "STRING")
        self.assertEqual(standardize_value_type((12, 34)), "INTARRAY")
