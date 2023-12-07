import subprocess
import re
import logging

import common.system_utils


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
        logging.error(f"Error: {e}")
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

        common.system_utils.restartNetworkServices()

        return True

    except Exception as e:
        logging.error(f"Error: {e}")
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
        logging.error(f"Error: {e}")
        return None, e
