import sys
import time
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger


logFilesFolder = "/opt/logs"

jsonFormatter = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def init_logger(service):
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
    logger.removeHandler(logger.handlers[0])
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    print(logger.handlers)
