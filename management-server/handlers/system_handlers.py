import json

import system_utils
import response_utils

def restartStickController(self):
    return_code, _ = system_utils.restartStickController()
    if return_code == 0:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)

def performUpgrade(self):
    return_code, _ = system_utils.runUpgrade()
    if return_code == 0:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)

def scanForNetworks(self):
    networks = system_utils.scan_wifi_networks()
    if networks == None:
        response_utils.InternalServerError(self, "Error scanning wireless networks")
    else:
        response_utils.okWithData(self, networks)

def connectToNetwork(self, post_data):
    json_data = json.loads(post_data.decode('utf-8'))
    ssid = json_data.get('ssid')
    psk = json_data.get('psk')
    key_mgmt = json_data.get('key_mgmt')

    success = system_utils.update_network_config(ssid, psk, key_mgmt)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "Error updating network configuration")

def getNetworkStatus(self):
    status = system_utils.get_wifi_connection_status()
    if status == None:
        response_utils.InternalServerError(self, "Error getting network connection status")
    else:
        response_utils.okWithData(self, status)
    