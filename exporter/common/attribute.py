import json
from typing import Union

from opentelemetry.sdk.resources import LabelValue, Attributes
from opentelemetry.util.types import Attributes as Another


def anyrobot_attributes_from_key_values(data: Union[Attributes, Another]) -> str:
    return json.dumps(
        [
            json.loads(anyrobot_attribute_from_key_value(key, data.get(key)))
            for key in data.keys()
        ]
    )


def anyrobot_attribute_from_key_value(key: str, value: LabelValue) -> str:
    return json.dumps(
        obj={
            "Key": key,
            "Value": {"Type": standardize_value_type(value), "Value": value},
        }
    )


def standardize_value_type(data: LabelValue) -> str:
    match str(type(data)):
        case "<class 'bool'>":
            return "BOOL"
        case "<class 'int'>":
            return "INT"
        case "<class 'float'>":
            return "FLOAT"
        case "<class 'str'>":
            return "STRING"
        case "<class 'tuple'>":
            if len(data) == 0:
                return "STRINGARRAY"
            return standardize_value_type(data[0]) + "ARRAY"
        case _:
            return str(type(data))
