import json

import system_utils
import response_utils


def restartStickController(self, query_parameters, match):
    return_code, _ = system_utils.restartStickController()
    if return_code == 0:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)


def performUpgrade(self, query_parameters, match):
    process, err = system_utils.runUpgrade()
    if err is None and process is not None:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)


def scanForNetworks(self, query_parameters, match):
    networks = system_utils.scan_wifi_networks()
    if networks is None:
        response_utils.InternalServerError(self, "Error scanning wireless networks")
    else:
        response_utils.okWithData(self, networks)


def connectToNetwork(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    ssid = json_data.get("ssid")
    psk = json_data.get("psk")
    key_mgmt = json_data.get("key_mgmt")

    success = system_utils.update_network_config(ssid, psk, key_mgmt)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "Error updating network configuration")


def getNetworkStatus(self, query_parameters, match):
    status, error = system_utils.get_wifi_connection_status()
    if error != None:
        response_utils.InternalServerError(
            self, "Error getting network connection status"
        )
    else:
        response_utils.okWithData(self, status)


def getApplicationVersions(self, query_parameters, match):
    versions = system_utils.get_versions()
    if versions is not None:
        response_utils.okWithData(self, versions)
    else:
        response_utils.InternalServerError(self, "Error getting application versions")


def getApplicationCurrentVersion(self, query_parameters, match):
    version = system_utils.get_current_version()
    if version is not None:
        response_utils.okWithData(self, version)
    else:
        response_utils.InternalServerError(
            self, "Error getting application current version"
        )


def switchApplicationVersion(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    version = json_data.get("version")

    success = system_utils.switch_version(version)
    if success is not None:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "Error switching application versions")
