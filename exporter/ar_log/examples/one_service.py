import time

from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import StdoutClient
from exporter.resource.resource import log_resource
from tlogging import SamplerLogger, Attributes
from tlogging.exporter import ConsoleExporter
from tlogging.tlogger import SyncLogger

if __name__ == "__main__":
    # print(time.time())
    # print(time.time_ns())
    # print(anyrobot_rfc3339_nano_from_unix_nano(time.time()))
    # print(anyrobot_rfc3339_nano_from_unix_nano(time.time_ns()))
    logger = SamplerLogger(log_resource(), ConsoleExporter())
    logger.loglevel = "TraceLevel"
    # 非结构化日志
    logger.trace("hello, this is threading test")
    # 结构化日志
    logger.trace({"a": 1, "b": 2}, etype="test")

    system_logger = SamplerLogger(log_resource(), ARLogExporter(StdoutClient("./AnyRobotLog1.txt")))
    system_logger.info("qwersdsdsad")
    system_logger.info({"a": 1, "b": 2}, etype="test", attributes=Attributes({"a": 1, "b": 2}, "test"))
    system_logger.info("qwersdsdsad")

    service_logger = SamplerLogger(log_resource(), ARLogExporter(StdoutClient("./AnyRobotLog2.txt")))
    service_logger.error("nothing")

    service_logger2 = SamplerLogger(log_resource(), ARLogExporter(StdoutClient("./AnyRobotLog3.txt")))
    service_logger2.error("867867")

    service_logger3 = SyncLogger(log_resource(), ARLogExporter(StdoutClient("./AnyRobotLog4.txt")))
    service_logger3.fatal(",.,.,.,..")
