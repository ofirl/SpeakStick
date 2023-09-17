import utils.system_utils
import utils.response_utils


def restartStickController(self, query_parameters, match):
    return_code, _ = utils.system_utils.restartStickController()
    if return_code == 0:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def performUpgrade(self, query_parameters, match):
    process, err = utils.system_utils.runUpgrade()
    if err is None and process is not None:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)
