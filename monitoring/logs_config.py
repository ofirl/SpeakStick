import sys
import time
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger


logFilesFolder = "/opt/logs"


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "fields"):
            record.fields = {}

        return super(CustomFormatter, self).format(record)


jsonFormatter = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s"
)


def init_logger(service):
    # create formatter
    formatter = CustomFormatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(fields)s - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(jsonFormatter)

    # file handler
    file_handler = logging.handlers.WatchedFileHandler(
        f"{logFilesFolder}/{service}.log"
    )
    # formatter.converter = time.gmtime  # if you want UTC time
    file_handler.setFormatter(jsonFormatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
