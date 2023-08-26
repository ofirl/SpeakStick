import subprocess
import os

from consts import words_directory

def restartStickController():
    return runCommand("sudo systemctl restart speakstick")

def runCommand(command):
    # Run the command and capture its output
    completed_process = subprocess.run(command, shell=True, text=True, capture_output=True)

    # Print the captured output
    output = completed_process.stdout
    print("Command output:")
    print(output)

    # Print the return code
    return_code = completed_process.returncode
    print("Return code:", return_code)

    return return_code, output

def getWordFiles():
    file_names = []
    for filename in os.listdir(words_directory):
        if os.path.isfile(os.path.join(words_directory, filename)):
            file_names.append(filename)
    return file_names