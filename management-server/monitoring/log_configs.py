import sys
import time
import logging
import logging.handlers

log_handler = logging.handlers.WatchedFileHandler("/opt/logs/management-server.log")
# create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
formatter.converter = time.gmtime  # if you want UTC time
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)

# 'application' code
logger.debug("debug message")
logger.info("info message")
logger.warning("warn message")
logger.error("error message")
logger.critical("critical message")
