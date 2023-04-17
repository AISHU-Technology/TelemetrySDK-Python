import os
import platform
import socket

from opentelemetry.sdk.resources import Resource, Attributes
from exporter.version.version import MetricInstrumentationName, MetricInstrumentationVersion, MetricInstrumentationURL
from opentelemetry.semconv.resource import ResourceAttributes
from tlogging.field import Resources


def default_service_name() -> str:
    service_name = os.path.abspath(__file__)
    if len(service_name) <= 0:
        return "UnknownServiceName"
    return service_name


globalServiceName = default_service_name()
globalServiceVersion = "UnknownServiceVersion"
globalServiceInstance = "UnknownServiceInstance"


def inner_attributes() -> Attributes:
    info = platform.uname()
    inner = {
        "host.ip": socket.gethostbyname(socket.gethostname()),
        ResourceAttributes.HOST_ARCH: info.machine,
        ResourceAttributes.HOST_NAME: info.node,
        ResourceAttributes.OS_TYPE: info.system,
        ResourceAttributes.OS_VERSION: info.version,
        ResourceAttributes.OS_DESCRIPTION: info.system + info.release,
        ResourceAttributes.SERVICE_NAME: globalServiceName,
        ResourceAttributes.SERVICE_VERSION: globalServiceVersion,
        ResourceAttributes.SERVICE_INSTANCE_ID: globalServiceInstance,
        ResourceAttributes.TELEMETRY_SDK_LANGUAGE: "python",
    }
    return inner


def metric_resource() -> Resource:
    attributes = inner_attributes()
    attributes[ResourceAttributes.TELEMETRY_SDK_NAME] = MetricInstrumentationName
    attributes[ResourceAttributes.TELEMETRY_SDK_VERSION] = MetricInstrumentationVersion
    return Resource.create(attributes=attributes, schema_url=MetricInstrumentationURL)


def log_resource() -> Resources:
    attributes = inner_attributes()
    attributes[ResourceAttributes.TELEMETRY_SDK_NAME] = MetricInstrumentationName
    attributes[ResourceAttributes.TELEMETRY_SDK_VERSION] = MetricInstrumentationVersion
    return Resources.create(attributes=attributes)
