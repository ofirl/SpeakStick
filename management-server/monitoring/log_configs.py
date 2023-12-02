import sys
import time
import logging
import logging.handlers

# create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

# console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# file handler
file_handler = logging.handlers.WatchedFileHandler("/opt/logs/management-server.log")
# formatter.converter = time.gmtime  # if you want UTC time
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)
