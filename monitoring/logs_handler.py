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

monitoring.logs_config.init_logger("logs-handler")

logFilesFolder = "/opt/logs"
servicesNames = ["stick-controller", "management-server"]  # TODO: add nginx?
logsEndpoint = "https://log-api.eu.newrelic.com/log/v1"
dummyApiKey = common.config_utils.get_config_value("LOGS_API_KEY")
deviceName = common.config_utils.get_config_value("DEVICE_NAME")
lastLogSampleTimeConfigKey = "LAST_LOG_SAMPLE"
currentVersion = common.versions_utils.get_current_version()
MAX_PAYLOAD_SIZE_BYTES = 1024


def get_logs(service):
    logFilePath = f"{logFilesFolder}/{service}.log"
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
            # Read lines until the target compressed size is reached
            while (
                len(gzip.compress(json.dumps([logs_chunk]).encode()))
                < target_compressed_size
            ):
                line = file.readline()
                if not line:
                    break

                logs_chunk["logs"].append(format_log(line))

            # Break if no more lines
            if not logs_chunk["logs"] or len(logs_chunk["logs"]) == 0:
                break

            # limit reached - output to a file
            lastLine = None
            # If we surpassed the limit we need to remove the last element
            if (
                len(gzip.compress(json.dumps([logs_chunk]).encode()))
                >= target_compressed_size
            ):
                lastLine = logs_chunk["logs"][-1]
                logs_chunk["logs"] = logs_chunk["logs"][:-1]

            output_file_path = f"{file_path}_chunk{chunk_number}.gz"
            with gzip.open(output_file_path, "wt", encoding="utf-8") as chunk_file:
                chunk_file.write(json.dumps([logs_chunk]))
            created_files.append(output_file_path)

            # If we surpassed the limit we need to add the last element to a new chunk
            if lastLine is not None:
                logs_chunk["logs"] = [lastLine]

            # new chunk
            chunk_number += 1

        # last iteration file output
        # Compress the lines and write to a gzip file
        if logs_chunk["logs"] and len(logs_chunk["logs"]) > 0:
            output_file_path = f"{file_path}_chunk{chunk_number}.gz"
            with gzip.open(output_file_path, "wt", encoding="utf-8") as chunk_file:
                chunk_file.write(json.dumps([logs_chunk]))
            created_files.append(output_file_path)

    return created_files


def write_file(file, data):
    with gzip.open(file, "wt", encoding="utf-8") as chunk_file:
        chunk_file.write(data)


def format_log(log):
    logParts = log.split(" - ", 3)
    # Extract timestamp and message from the log line
    timestamp_str, level, filePath, message = (
        logParts[0],
        logParts[1],
        logParts[2],
        logParts[3],
    )

    # Convert the timestamp string to a datetime object
    timestamp = datetime.strptime(f"{''.join(timestamp_str)}", "%Y-%m-%d %H:%M:%S")

    # Convert the datetime object to Unix timestamp
    timestamp_unix = int(timestamp.timestamp())

    timestamp = int(timestamp_unix)
    log_entry = {
        "timestamp": timestamp,
        "message": message.strip(" \n"),
        "attributes": {"level": level, "file": filePath},
    }

    return log_entry


def format_logs(logs):
    formatted_logs = []

    # Replace this with your logic to parse and format the raw logs
    # The following is just a placeholder, modify it according to your log structure
    for line in logs:
        formatted_logs.append(format_log(line))

    return formatted_logs


def send_logs(data_file):
    try:
        with open(data_file, "r", encoding="utf-8") as file:
            # Send formatted logs over HTTP with API key header
            headers = {"API-key": dummyApiKey, "Content-Type": "application/json"}
            response = requests.post(
                logsEndpoint,
                data=file.read().encode(),
                headers=headers,
            )

            if response.status_code % 100 == 2:
                os.remove(data_file)
                logging.debug(f"status code: {response.status_code}")
            else:
                logging.debug(
                    f"Failed to send logs. HTTP Status Code: {response.status_code}"
                )
    except Exception as e:
        logging.error(f"Error sending logs: {e}")


for service in servicesNames:
    logging.info(f"Starting logs collection for ${service}")
    logs, file_path = get_logs(service)
    if logs:
        chunks = split_file(file_path, MAX_PAYLOAD_SIZE_BYTES, service)
        for chunk_file in chunks:
            send_logs(chunk_file)
