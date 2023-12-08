import sys
import time
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger

import common.config_utils

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
    # remove the default StreamHandler if exists
    if len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])

    # add the custom handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # set log level
    if service == "logs-handler":
        loggingLevel = common.config_utils.get_config_value(
            "LOGS_HANDLER_LOGGING_LEVEL"
        )
    else:
        loggingLevel = common.config_utils.get_config_value("LOGGING_LEVEL")
    if loggingLevel is None:
        loggingLevel = "INFO"
    logger.setLevel(logging._nameToLevel[loggingLevel])
