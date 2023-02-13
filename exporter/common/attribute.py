import json
from typing import Union

from opentelemetry.sdk.resources import LabelValue, Attributes, Resource
from opentelemetry.util.types import Attributes as Another


def anyrobot_resource_from_resource(data: Resource) -> str:
    return json.dumps(
        obj=json.loads(anyrobot_attributes_from_key_values(data.attributes)),
        ensure_ascii=False,
    )


def anyrobot_attributes_from_key_values(data: Union[Attributes, Another]) -> str:
    return json.dumps(
        obj=[
            json.loads(anyrobot_attribute_from_key_value(key, data.get(key)))
            for key in data.keys()
        ],
        ensure_ascii=False,
    )


def anyrobot_attribute_from_key_value(key: str, value: LabelValue) -> str:
    return json.dumps(
        obj={
            "Key": key,
            "Value": {"Type": standardize_value_type(value), "Value": value},
        },
        ensure_ascii=False,
    )


def standardize_value_type(data: LabelValue) -> str:
    """
    standardize_value_type 标准化统一 value_type 为各语言统一格式。
    """
    if str(type(data)) == "<class 'bool'>":
        return "BOOL"
    if str(type(data)) == "<class 'int'>":
        return "INT"
    if str(type(data)) == "<class 'float'>":
        return "FLOAT"
    if str(type(data)) == "<class 'str'>":
        return "STRING"
    if str(type(data)) == "<class 'tuple'>":
        if len(data) == 0:
            return "STRINGARRAY"
        return standardize_value_type(data[0]) + "ARRAY"

    return str(type(data))
