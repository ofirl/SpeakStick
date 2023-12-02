import subprocess
import requests
import time
import json

from datetime import datetime

import utils.system_utils

servicesNames = ["speakstick", "speakstick-management-server", "nginx"]
logsEndpoint = "https://log-api.eu.newrelic.com/log/v1"
dummyApiKey = "eu01xx7972418d9f4ca7b4907ff16931FFFFNRAL"


def get_logs():
    returnCode, output = utils.system_utils.runCommand(
        [
            'journalctl --no-pager -u speakstick --since "5 minutes ago"',
            # '"2015-06-26 23:15:00"'
        ]
    )
    return output


def format_logs(logs):
    formatted_logs = []

    # Replace this with your logic to parse and format the raw logs
    # The following is just a placeholder, modify it according to your log structure
    for line in logs.splitlines()[1:]:
        # Extract timestamp and message from the log line
        timestamp_str, message = line.split(" ", 5)[0:3], " ".join(
            line.split(" ", 5)[5:]
        )

        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(
            f"{datetime.now().year} {' '.join(timestamp_str)}", "%Y %b %d %H:%M:%S"
        )

        # Convert the datetime object to Unix timestamp
        timestamp_unix = int(timestamp.timestamp())

        timestamp = int(timestamp_unix)
        log_entry = {"timestamp": timestamp, "message": message}
        formatted_logs.append(log_entry)

    return formatted_logs


def send_logs(logs):
    try:
        # Format logs to the desired structure
        formatted_logs = [
            {
                "common": {
                    "attributes": {
                        "logtype": "accesslogs",
                        "service": "login-service",
                        "hostname": "login.example.com",
                    }
                },
                "logs": format_logs(logs),
            }
        ]

        # print(f"formatted_logs: {formatted_logs}")

        # Send formatted logs over HTTP with API key header
        headers = {"API-key": dummyApiKey, "Content-Type": "application/json"}
        response = requests.post(
            logsEndpoint, data=json.dumps(formatted_logs), headers=headers
        )

        if response.status_code == 200:
            print("Logs sent successfully")
        else:
            print(f"Failed to send logs. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending logs: {e}")


def logLoop():
    while True:
        logs = get_logs()
        if logs:
            send_logs(logs)

        # Wait for 1 minute before fetching and sending logs again
        time.sleep(60)
