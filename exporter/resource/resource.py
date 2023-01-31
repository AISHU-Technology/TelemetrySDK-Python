from opentelemetry.sdk.resources import Resource, Attributes

from exporter.version.version import *


def default_service_name() -> str:
    return "UnknownServiceName"


globalServiceName = default_service_name()
globalServiceVersion = "UnknownServiceVersion"
globalServiceInstance = "UnknownServiceInstance"


def inner_attributes() -> Attributes:
    inner = {
        "host.ip": "",
        "host.arch": "",
        "host.name": "",
        "os.type": "",
        "os.version": "",
        "os.description": "",
        "service.name": globalServiceName,
        "service.version": globalServiceVersion,
        "service.instance.id": globalServiceInstance,
        "telemetry.sdk.language": "python",
    }
    return inner


def metric_resource() -> Resource:
    attributes = inner_attributes()
    attributes["telemetry.sdk.name"] = MetricInstrumentationName
    attributes["telemetry.sdk.version"] = MetricInstrumentationVersion
    return Resource.create(attributes=attributes, schema_url=MetricInstrumentationURL)
