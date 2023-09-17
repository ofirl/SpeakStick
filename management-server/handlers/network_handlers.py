import json

import utils.network_utils
import utils.response_utils


def scanForNetworks(self, query_parameters, match):
    networks = utils.network_utils.scan_wifi_networks()
    if networks is None:
        utils.response_utils.InternalServerError(
            self, "Error scanning wireless networks"
        )
    else:
        utils.response_utils.okWithData(self, networks)


def connectToNetwork(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    ssid = json_data.get("ssid")
    psk = json_data.get("psk")
    key_mgmt = json_data.get("key_mgmt")

    success = utils.network_utils.update_network_config(ssid, psk, key_mgmt)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(
            self, "Error updating network configuration"
        )


def getNetworkStatus(self, query_parameters, match):
    status, error = utils.network_utils.get_wifi_connection_status()
    if error is not None:
        utils.response_utils.InternalServerError(
            self, "Error getting network connection status"
        )
    else:
        utils.response_utils.okWithData(self, status)
