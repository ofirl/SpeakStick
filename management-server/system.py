import subprocess
import re
import os

from consts import words_directory

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

def restartStickController():
    return runCommand("sudo systemctl restart speakstick")

def runUpgrade():
    return runCommand("/opt/SpeakStick/upgrade-script.sh")

def getWordFiles():
    file_names = []
    for filename in os.listdir(words_directory):
        if os.path.isfile(os.path.join(words_directory, filename)):
            file_names.append(filename)
    return file_names

# network names and pass keys are saved in "/etc/wpa_supplicant/wpa_supplicant.conf"
def scan_wifi_networks():
    try:
        # Run the command and capture its output
        output = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"], stderr=subprocess.STDOUT, text=True)

        # Initialize a list to store network information dictionaries
        networks = []

        # Define regex patterns to extract SSID and encryption info
        ssid_pattern = re.compile(r'ESSID:"(.*)"')
        encryption_pattern = re.compile(r'Encryption key:(on|off)')
        wpa2_pattern = re.compile(r'IE: IEEE 802.11i/WPA2')
        wpa3_pattern = re.compile(r'IE: IEEE 802.11i/WPA3')

        # Split the output into individual network sections
        network_sections = output.split("Cell ")

        # Loop through each network section and extract information
        for section in network_sections[1:]:
            network_info = {}
            ssid_match = ssid_pattern.search(section)
            encryption_match = encryption_pattern.search(section)
            wpa2_match = wpa2_pattern.search(section)
            wpa3_match = wpa3_pattern.search(section)

            if ssid_match:
                network_info["ssid"] = ssid_match.group(1)
            else:
                continue

            if encryption_match:
                network_info["secured"] = (encryption_match.group(1) == "on")
            else:
                network_info["secured"] = False

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
        return []

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
                            updated_lines.append('network={\n')
                            updated_lines.append(f'    ssid="{ssid}"\n')
                            updated_lines.append(f'    psk="{psk}"\n')
                            if key_mgmt:
                                updated_lines.append(f'    key_mgmt={key_mgmt}\n')
                            updated_lines.append('}\n')
                        else:
                            updated_lines.append(network_config + "\n")
                    else:
                        updated_lines.append(network_config + "\n")
            else:
                updated_lines.append(line + "\n")

        # If the SSID is not found, add a new network configuration
        if not found_ssid:
            updated_lines.append('network={\n')
            updated_lines.append(f'    ssid="{ssid}"\n')
            updated_lines.append(f'    psk="{psk}"\n')
            if key_mgmt:
                updated_lines.append(f'    key_mgmt={key_mgmt}\n')
            updated_lines.append('}\n')

        # Write the updated content back to the file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.writelines(updated_lines)

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False