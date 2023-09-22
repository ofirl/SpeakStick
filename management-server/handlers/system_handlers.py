import utils.system_utils
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
