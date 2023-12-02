import subprocess
import requests
import time
import json
import math
import os

from datetime import datetime

import utils.system_utils
import utils.db_utils
import utils.versions_utils

logFilesFolder = "/opt/logs"
# nginx?
servicesNames = ["stick-controller", "management-server"]
logsEndpoint = "https://log-api.eu.newrelic.com/log/v1"
dummyApiKey = utils.db_utils.get_config_value("LOGS_API_KEY")
deviceName = utils.db_utils.get_config_value("DEVICE_NAME")
lastLogSampleTimeConfigKey = "LAST_LOG_SAMPLE"
currentVersion = utils.versions_utils.get_current_version()


def get_logs(service):
    logFilePath = f"{logFilesFolder}/{service}.log"
    if not os.path.exists(logFilePath):
        return None

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

    return lines


def format_logs(logs):
    formatted_logs = []

    # Replace this with your logic to parse and format the raw logs
    # The following is just a placeholder, modify it according to your log structure
    for line in logs.splitlines()[1:]:
        if line == "-- No entries --":
            return []

        # Extract timestamp and message from the log line
        timestamp_str, message = line.split(" ", 5)[0:3], " ".join(
            line.split(" ", 5)[5:]
        )

        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(
            f"{datetime.now().year} {' '.join(timestamp_str)}", "%Y-%m-%d %H:%M:%S"
        )

        # Convert the datetime object to Unix timestamp
        timestamp_unix = int(timestamp.timestamp())

        timestamp = int(timestamp_unix)
        log_entry = {"timestamp": timestamp, "message": message}
        formatted_logs.append(log_entry)

    return formatted_logs


def send_logs(logs, service, sampleTime):
    # send logs in chunks in case there are a lot of unsent logs
    # logChunkSize = 10
    # for i in range(0, len(logs), logChunkSize):
    # chunk = logs[i : i + logChunkSize]
    chunk = logs
    try:
        # Format logs to the desired structure
        formatted_logs = [
            {
                "common": {
                    "attributes": {
                        # "logtype": "accesslogs",
                        "application": "SpeakStick",
                        "service": service,
                        "hostname": deviceName,
                        "version": currentVersion,
                    }
                },
                "logs": format_logs(chunk),
            }
        ]

        if len(formatted_logs[0]["logs"]) == 0:
            return

        # Send formatted logs over HTTP with API key header
        headers = {"API-key": dummyApiKey, "Content-Type": "application/json"}
        response = requests.post(
            logsEndpoint, data=json.dumps(formatted_logs), headers=headers
        )

        if response.status_code % 100 == 2:
            utils.db_utils.update_config(lastLogSampleTimeConfigKey, sampleTime, False)
        else:
            print(f"Failed to send logs. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending logs: {e}")


def logLoop():
    while True:
        for service in servicesNames:
            sampleTime = time.time()
            logs = get_logs(service)
            if logs:
                send_logs(logs, service, sampleTime)

        # Wait for 1 minute before fetching and sending logs again
        time.sleep(20)
