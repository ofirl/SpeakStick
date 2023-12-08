import sys

sys.path.append("/opt/SpeakStick")  # Adds higher directory to python modules path.

import re
import requests
import time
import json
import os
import logging
import gzip

from datetime import datetime

import monitoring.logs_config

import common.config_utils
import common.versions_utils
import common.system_utils

monitoring.logs_config.init_logger("logs-handler")

servicesNames = [
    "stick-controller",
    "management-server",
    "logs-handler",
    "upgrade",
    "nginx",
]
logsEndpoint = "https://log-api.eu.newrelic.com/log/v1"
logsApiKey = common.config_utils.get_config_value("LOGS_API_KEY")
deviceName = common.config_utils.get_config_value("DEVICE_NAME")
lastLogSampleTimeConfigKey = "LAST_LOG_SAMPLE"
currentVersion = common.versions_utils.get_current_version()
MAX_PAYLOAD_SIZE_BYTES = 1000000


def getLogFileName(service):
    return f"{monitoring.logs_config.logFilesFolder}/{service}.log"


def getChunkFileName(service, chunk_number):
    return f"{getLogFileName(service)}.old_chunk{chunk_number}.gz"


def get_logs(service):
    logFilePath = getLogFileName(service)
    if not os.path.exists(logFilePath):
        return None, None

    # this is here because we might have failed sending the logs previously
    # what this is doing is appending the new logs to the old logs
    renamedLogFilePath = f"{logFilePath}.old"
    if os.path.exists(renamedLogFilePath):
        tempLogFilePath = f"{renamedLogFilePath}2"
        os.rename(logFilePath, tempLogFilePath)

        with open(tempLogFilePath, "r") as old_log_file:
            lines = old_log_file.readlines()
            with open(renamedLogFilePath, "w") as log_file:
                for line in lines:
                    log_file.write(line)

        os.remove(tempLogFilePath)
    else:
        os.rename(logFilePath, renamedLogFilePath)

    if service == "nginx":
        # reload nginx log files and let it complete the rotation
        common.system_utils.runCommand("kill -USR1 `cat /var/run/nginx.pid`")
        time.sleep(1)
        # with open(logFilePath, "w") as nginx_new_log_file:
        #     logging.debug("Created a new log file for nginx")

    with open(renamedLogFilePath, "r") as log_file:
        lines = log_file.readlines()

    return lines, renamedLogFilePath


def split_file(file_path, target_compressed_size, service):
    created_files = []
    with open(file_path, "r", encoding="utf-8") as file:
        chunk_number = 1
        logs_chunk = {
            "common": {
                "attributes": {
                    "application": "SpeakStick",
                    "service": service,
                    "hostname": deviceName,
                    "version": currentVersion,
                }
            },
            "logs": [],
        }

        while True:
            output_file_path = getChunkFileName(service, chunk_number)
            while os.path.exists(output_file_path):
                chunk_number += 1
                output_file_path = getChunkFileName(service, chunk_number)

            # Read lines until the target compressed size is reached
            while (
                len(gzip.compress(json.dumps([logs_chunk]).encode()))
                < target_compressed_size
            ):
                line = file.readline()
                if not line:
                    logging.debug(f"file ended, exiting")
                    break

                formatted_line = format_log(line, service)
                logging.debug(f"adding line to chunk", extra={"line": formatted_line})
                logs_chunk["logs"].append(formatted_line)

            # Break if no more lines
            if not logs_chunk["logs"] or len(logs_chunk["logs"]) == 0:
                logging.debug(f"no lines in chunk, exiting")
                break

            # limit reached - output to a file
            lastLine = None
            # If we surpassed the limit we need to remove the last element
            chunkSize = len(gzip.compress(json.dumps([logs_chunk]).encode()))
            logging.debug(f"checking chunk size", extra={"chunk_size": chunkSize})
            if chunkSize >= target_compressed_size:
                logging.debug(f"we surpassed the limit")
                lastLine = logs_chunk["logs"][-1]
                logs_chunk["logs"] = logs_chunk["logs"][:-1]

            logging.debug(
                f"writing to file", extra={"output_file_path": output_file_path}
            )
            with gzip.open(output_file_path, "wt", encoding="utf-8") as chunk_file:
                chunk_file.writelines(json.dumps([logs_chunk]))
            logging.debug(
                f"chunk file created", extra={"output_file_path": output_file_path}
            )
            created_files.append(output_file_path)

            # If we surpassed the limit we need to add the last element to a new chunk
            if lastLine is not None:
                logging.debug(
                    f"bring back last line because we surpassed the limit",
                    extra={"line": lastLine},
                )
                logs_chunk["logs"] = [lastLine]
            else:
                logs_chunk["logs"] = []

            # new chunk
            chunk_number += 1
            logging.debug("strating a new chunk", extra={"chunk_number": chunk_number})

        # last iteration file output
        # Compress the lines and write to a gzip file
        if logs_chunk["logs"] and len(logs_chunk["logs"]) > 0:
            output_file_path = getChunkFileName(service, chunk_number)
            with gzip.open(output_file_path, "wt", encoding="utf-8") as chunk_file:
                chunk_file.write(json.dumps([logs_chunk]))
            created_files.append(output_file_path)

    logging.debug(f"log file split", extra={"fields": {"created_files": created_files}})
    os.remove(file_path)

    return created_files


def write_file(file, data):
    with gzip.open(file, "wt", encoding="utf-8") as chunk_file:
        chunk_file.write(data)


def extract_timestamp_from_nginx_log(log_line):
    log_pattern = re.compile(r"\[([^\]]+)\]")

    match = log_pattern.search(log_line)
    if match:
        timestamp_str = match.group(1)
        # Convert timestamp to ISO format
        timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        return timestamp
    else:
        return None


def parse_nginx_log(log_line):
    log_pattern = re.compile(
        r'(?P<ip>[\w.:]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>[^"?]+)\??(?P<query>.*?) (?P<protocol>.*?)" (?P<status>\d+) (?P<size>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"'
    )

    match = log_pattern.match(log_line)
    if match:
        log_data = match.groupdict()

        # Convert timestamp to ISO format
        log_data["timestamp"] = datetime.strptime(
            log_data["timestamp"], "%d/%b/%Y:%H:%M:%S %z"
        ).timestamp()

        # Convert size to integer
        log_data["size"] = int(log_data["size"])

        log_data["logtype"] = "nginx"
        log_data["message"] = log_line
        return log_data
    else:
        return None


def format_log(log, service=None):
    try:
        # nginx has a special format
        if service == "nginx":
            # log_entry = parse_nginx_log(log)
            log_entry = {"message": log.strip(" \n"), "logtype": "nginx"}
            return log_entry

        # upgrade is a shell script without any special formatting
        if service == "upgrade":
            log_entry = {
                "timestamp": int(datetime.now().timestamp()),
                "message": log.strip(" \n"),
            }
            return log_entry

        logParts = json.loads(log)

        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(logParts["asctime"], "%Y-%m-%d %H:%M:%S")

        # Convert the datetime object to Unix timestamp
        timestamp = int(timestamp.timestamp())
        log_entry = {
            "timestamp": timestamp,
            "message": logParts["message"].strip(" \n"),
            "attributes": {
                "level": logParts["levelname"],
                "file": f"{logParts['filename']}:{logParts['lineno']}",
            },
        }

        reservedKeys = ["asctime", "message", "levelname", "filename", "lineno", "name"]
        for attr, value in logParts.items():
            if attr not in reservedKeys:
                log_entry["message"] = f"{log_entry['message']}, {attr}={value}"

    except Exception as e:
        logging.exception("Error formatting log")
        log_entry = {
            "timestamp": int(datetime.now().timestamp()),
            "message": log.strip(" \n"),
        }

    return log_entry


def send_logs(service):
    if not logsApiKey or logsApiKey == "":
        logging.warning("No logs api key found")
        return

    chunk_number = 1
    data_file = getChunkFileName(service, chunk_number)
    while os.path.exists(data_file):
        try:
            logging.debug(
                f"sending log chunk",
                extra={
                    "service": service,
                    "chunk_number": chunk_number,
                    "chunk_file": data_file,
                },
            )
            with gzip.open(data_file, "r") as file:
                # Send formatted logs over HTTP with API key header
                headers = {"API-key": logsApiKey, "Content-Type": "application/json"}
                response = requests.post(
                    logsEndpoint,
                    data=file.read(),
                    headers=headers,
                )

                if response.status_code % 100 == 2:
                    os.remove(data_file)
                    logging.debug(
                        f"status code", extra={"responseCode": response.status_code}
                    )
                else:
                    logging.debug(
                        f"Failed to send logs",
                        extra={
                            "responseCode": response.status_code,
                            "responseText": response.text,
                            "responseRaw": response.raw,
                        },
                    )

        except Exception as e:
            logging.error(f"Error sending logs: {e}")

        chunk_number += 1
        data_file = getChunkFileName(service, chunk_number)


for service in servicesNames:
    logging.info(f"Starting logs collection", extra={"service": service})
    logs, file_path = get_logs(service)
    logging.debug(f"log file saved", extra={"service": service})
    if logs and file_path:
        logging.debug(f"splitting log file", extra={"service": service})
        split_file(file_path, MAX_PAYLOAD_SIZE_BYTES, service)
        send_logs(service)
