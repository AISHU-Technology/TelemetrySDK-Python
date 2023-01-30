import json

from opentelemetry.sdk.resources import Resource

from exporter.common.attribute import anyrobot_attributes_from_key_values


def anyrobot_resource_from_resource(data: Resource) -> str:
    return json.dumps(
        obj=json.loads(anyrobot_attributes_from_key_values(data.attributes))
        # dict(data.attributes),
    )
