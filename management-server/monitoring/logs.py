import subprocess
import requests
import time

import utils.system_utils

servicesNames = ["speakstick", "speakstick-management-server", "nginx"]
logsEndpoint = "https://log-api.eu.newrelic.com/log/v1"
dummyApiKey = "eu01xxf47e6ba1424af8129e30afbd4fFFFFNRAL"


def get_logs():
    returnCode, output = utils.system_utils.runCommand(
        [
            "journalctl",
            "-u",
            "speakstick-management-server",
            "--since",
            # '"2015-06-26 23:15:00"',
            "1 hour ago",
            "--no-pager",
        ]
    )
    return output


def send_logs(logs):
    try:
        # Send logs over HTTP
        headers = {"Api-Key": dummyApiKey}
        response = requests.post(logsEndpoint, data=logs, headers=headers)
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
        time.sleep(10)
