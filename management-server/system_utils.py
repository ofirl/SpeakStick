import subprocess
import re
import os
import git

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
        return None, None


def restartNetworkServices():
    return runCommand("sleep 3 && sudo systemctl restart dnsmasq hostapd dhcpcd &")


def restartStickController():
    return runCommand("sudo systemctl restart speakstick")


def runUpgrade():
    return runCommandBackground("/opt/SpeakStick/upgrade-script.sh")


def getWordFiles():
    file_names = []
    for filename in os.listdir(words_directory):
        if os.path.isfile(os.path.join(words_directory, filename)):
            file_names.append(filename)
    return file_names


def signalStrengthToNumber(strength: int):
    return min(max(4 + (strength + 60) // 10, 0), 4)


# network names and pass keys are saved in "/etc/wpa_supplicant/wpa_supplicant.conf"
def scan_wifi_networks():
    try:
        # Run the command and capture its output
        output = subprocess.check_output(
            ["sudo", "iwlist", "wlan0", "scan"], stderr=subprocess.STDOUT, text=True
        )

        # Initialize a list to store network information dictionaries
        networks = []

        # Define regex patterns to extract SSID and encryption info
        ssid_pattern = re.compile(r'ESSID:"(.*)"')
        encryption_pattern = re.compile(r"Encryption key:(on|off)")
        signal_level_pattern = re.compile(r"Signal level=(-\d+) dBm")
        wpa2_pattern = re.compile(r"IE: IEEE 802.11i/WPA2")
        wpa3_pattern = re.compile(r"IE: IEEE 802.11i/WPA3")

        # Split the output into individual network sections
        network_sections = output.split("Cell ")

        # Loop through each network section and extract information
        for section in network_sections[1:]:
            network_info = {}
            ssid_match = ssid_pattern.search(section)
            encryption_match = encryption_pattern.search(section)
            signal_match = signal_level_pattern.search(section)
            wpa2_match = wpa2_pattern.search(section)
            wpa3_match = wpa3_pattern.search(section)

            if ssid_match:
                network_info["ssid"] = ssid_match.group(1)
            else:
                continue

            if encryption_match:
                network_info["secured"] = encryption_match.group(1) == "on"
            else:
                network_info["secured"] = False

            if signal_match:
                signal_level_dbm = int(signal_match.group(1))
                network_info["signal_strength"] = signalStrengthToNumber(
                    signal_level_dbm
                )
            else:
                network_info["signal_strength"] = 0

            if wpa2_match:
                network_info["key_mgmt"] = "WPA2"
            elif wpa3_match:
                network_info["key_mgmt"] = "WPA3"
            else:
                network_info["key_mgmt"] = "None"

            networks.append(network_info)

        return networks

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def update_network_config(ssid, psk, key_mgmt=None):
    try:
        # Read the wpa_supplicant.conf file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as f:
            lines = f.readlines()

        # Initialize variables to track network configuration
        in_network_block = False
        found_ssid = False
        updated_lines = []
        network_block = []

        # Iterate through the lines in the file
        for line in lines:
            line = line.strip()
            if line.startswith("network={"):
                in_network_block = True
                network_block = [line]
            elif in_network_block:
                network_block.append(line)
                if line == "}":
                    in_network_block = False
                    network_config = "\n".join(network_block)
                    # Extract SSID from the network configuration
                    ssid_match = re.search(r'ssid="(.*)"', network_config)
                    if ssid_match:
                        existing_ssid = ssid_match.group(1)
                        if existing_ssid == ssid:
                            found_ssid = True
                            # Update the existing network configuration
                            updated_lines.append("network={\n")
                            updated_lines.append(f'    ssid="{ssid}"\n')
                            updated_lines.append(f'    psk="{psk}"\n')
                            if key_mgmt:
                                if key_mgmt.startswith("WPA"):
                                    updated_lines.append(f"    key_mgmt=WPA-PSK\n")
                            updated_lines.append("}\n")
                        else:
                            updated_lines.append(network_config + "\n")
                    else:
                        updated_lines.append(network_config + "\n")
            else:
                updated_lines.append(line + "\n")

        # If the SSID is not found, add a new network configuration
        if not found_ssid:
            updated_lines.append("network={\n")
            updated_lines.append(f'    ssid="{ssid}"\n')
            updated_lines.append(f'    psk="{psk}"\n')
            if key_mgmt:
                if key_mgmt.startswith("WPA"):
                    updated_lines.append(f"    key_mgmt=WPA-PSK\n")
            updated_lines.append("}\n")

        # Write the updated content back to the file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.writelines(updated_lines)

        restartNetworkServices()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_wifi_connection_status(interface="wlan0"):
    try:
        # Run the iwconfig command for the specified interface
        output = subprocess.check_output(
            ["iwconfig", interface], stderr=subprocess.STDOUT, text=True
        )

        # Define regex patterns to extract SSID and Signal level information
        essid_pattern = re.compile(r'ESSID:"(.*?)"')
        signal_level_pattern = re.compile(r"Signal level=(-\d+) dBm")

        # Search for ESSID and Signal level in the output
        essid_match = essid_pattern.search(output)
        signal_level_match = signal_level_pattern.search(output)

        connection_status = {}

        if essid_match:
            connection_status["ssid"] = essid_match.group(1)
        else:
            return None, None

        if signal_level_match:
            # Extract the signal level in dBm and convert it to a strength value between 0 and 4
            signal_level_dbm = int(signal_level_match.group(1))
            # Calculate the signal strength value (assuming a reasonable dBm range)
            signal_strength = signalStrengthToNumber(signal_level_dbm)
        else:
            # If no signal level information is found, assume no signal (0 strength)
            signal_strength = 0

        connection_status["signal_strength"] = signal_strength

        return connection_status, None

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, e


def switch_version(version):
    try:
        code, _ = runCommand(f"cd /opt/SpeakStick && git checkout {version}")
        return code != 0

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_versions():
    try:
        repo = git.Repo(search_parent_directories=True)
        print(repo)
        tags = [str(tag) for tag in repo.tags]
        print(tags)
        return tags

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# def get_versions():
#     try:
#         code, output = runCommand(f"cd /opt/SpeakStick && git tag -l")
#         if code != 0:
#             raise BaseException(
#                 f"Error getting tags, return code: {code}, output: {output}"
#             )

#         return output
#     except Exception as e:
#         print(f"Error: {e}")
#         return False
