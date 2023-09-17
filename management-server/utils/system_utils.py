import subprocess
import os

from consts import words_directory


def runCommand(command):
    # Run the command and capture its output
    completed_process = subprocess.run(
        command, shell=True, text=True, capture_output=True
    )

    # Print the captured output
    output = completed_process.stdout
    print("Command output:")
    print(output)

    # Print the return code
    return_code = completed_process.returncode
    print("Return code:", return_code)

    return return_code, output


def runCommandBackground(command):
    try:
        # Use subprocess.Popen to run the command in the background
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Optionally, you can capture the process ID (PID) if you need it
        pid = process.pid

        # Print the PID and command
        print(f"Command '{command}' started in the background with PID: {pid}")

        return process, None

        # You can wait for the command to complete (optional)
        # process.wait()

        # you can capture and print the command's output
        # stdout, stderr = process.communicate()
        # print(f"Command output:\n{stdout.decode('utf-8')}")

    except Exception as e:
        print(f"Error running command '{command}': {str(e)}")
        return None, e


def restartNetworkServices():
    return runCommand("sleep 3 && sudo systemctl restart dnsmasq hostapd dhcpcd &")


def restartStickController():
    return runCommand("sudo systemctl restart speakstick")


def runUpgrade(version=""):
    return runCommandBackground(f"/opt/SpeakStick/upgrade-script.sh {version}")


def getWordFiles():
    file_names = []
    for filename in os.listdir(words_directory):
        if os.path.isfile(os.path.join(words_directory, filename)):
            file_names.append(filename)
    return file_names


def resetToFactorySettings():
    try:
        code, output = runCommand("sudo rm /opt/SpeakStick/configs.db")
        if code != 0:
            raise BaseException("Error clearing DB")

        code, output = restartStickController()
        if code != 0:
            raise BaseException("Error restarting stick controller")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return True
