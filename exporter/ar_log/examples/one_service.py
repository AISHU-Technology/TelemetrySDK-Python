from tlogging import SamplerLogger, Attributes

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import HTTPClient, StdoutClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode
from exporter.resource.resource import log_resource, set_service_info
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger

if __name__ == "__main__":
    set_service_info("YourServiceName", "2.3.0", "983d7e1d5e8cda64")
    system_logger = SamplerLogger(log_resource(), ConsoleExporter(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://10.4.130.68/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events"))))
    func_attr = Attributes({"age": 18}, atype="person")
    system_logger.info(message="this is a info message", attributes=func_attr)
    system_logger.warn(message={"age": 18}, etype="person")
    system_logger.error("something error")

    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://10.4.130.68/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    err = service_logger.info("this is a info message")
    if err:
        print("something went wrong")
