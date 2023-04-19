from tlogging import SamplerLogger

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import HTTPClient, StdoutClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode
from exporter.resource.resource import log_resource
from tlogging.tlogger import SyncLogger

if __name__ == "__main__":
    system_logger = SamplerLogger(log_resource(), ARLogExporter(StdoutClient()))
    system_logger.info("this is a info message")
    system_logger.warn({"age": 18}, etype="person")

    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://127.0.0.1/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    err = service_logger.error("this is a error message")
    if err:
        print("something went wrong")
