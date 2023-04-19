from tlogging import SamplerLogger

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import HTTPClient, StdoutClient
from exporter.public.public import WithAnyRobotURL, WithSyncMode
from exporter.resource.resource import log_resource
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger

if __name__ == "__main__":
    system_logger = SamplerLogger(log_resource(), ConsoleExporter(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://10.4.130.68/api/feed_ingester/v1/jobs/job-983d7e1d5e8cda64/events"))))
    system_logger.info("this is a info message")
    system_logger.warn({"age": 18}, etype="person")
    system_logger.error("error")
    system_logger.fatal("fatal")

    service_logger = SyncLogger(log_resource(), ARLogExporter(
        HTTPClient(WithAnyRobotURL("http://10.4.130.68/api/feed_ingester/v1/jobs/job-c9a577c302505576/events"),
                   WithSyncMode())))

    err = service_logger.info("this is a info message")
    if err:
        print("something went wrong")
    err = service_logger.warn("this is a warn message")
    if err:
        print("something went wrong")
    err = service_logger.error("this is a error message")
    if err:
        print("something went wrong")
    err = service_logger.fatal("this is a fatal message")
    if err:
        print("something went wrong")
