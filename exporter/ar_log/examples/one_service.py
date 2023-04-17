from exporter.ar_log.log_exporter import ARLogExporter
from exporter.public.client import StdoutClient
from tlogging import SamplerLogger

if __name__ == "__main__":
    logger = SamplerLogger()
    logger.loglevel = "TraceLevel"
    # 非结构化日志
    logger.trace("hello, this is threading test")
    # 结构化日志
    logger.trace({"a": 1, "b": 2}, etype="test")

    system_logger = SamplerLogger(ARLogExporter(StdoutClient("./AnyRobotLog.txt")))
    system_logger.info("message")
