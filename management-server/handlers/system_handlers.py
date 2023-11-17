import json
import utils.system_utils
import utils.battery_utils
import utils.response_utils


def restartStickController(self, query_parameters, match):
    return_code, _ = utils.system_utils.restartStickController()
    if return_code == 0:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def resetToFactorySettings(self, query_parameters, match):
    success = utils.system_utils.resetToFactorySettings()
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def setAudioOutput(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    card_number = json_data.get("card_number")

    success, error = utils.system_utils.write_default_sound_config(card_number)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(
            self, f"Error updating audio output: {error}"
        )


def getBatteryPercent(self, query_parameters, match):
    percent, isCharging = utils.battery_utils.getBatteryPercent()
    if percent is not None:
        utils.response_utils.okWithData(
            self, {"percent": percent, "isCharging": isCharging}
        )
    else:
        utils.response_utils.InternalServerError(self)


def getServiceLogs(self, query_parameters, match):
    service = match.group("service")
    if query_parameters is not None:
        lines = query_parameters.get("lines")
        if lines is None:
            lines = 200
    else:
        lines = 200

    serviceLogs = utils.system_utils.get_services_logs(service, lines)
    if serviceLogs is not None:
        utils.response_utils.okWithData(self, serviceLogs)
    else:
        utils.response_utils.InternalServerError(self)
