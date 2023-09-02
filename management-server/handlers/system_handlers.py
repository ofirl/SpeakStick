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