import db_utils

import response_utils

def getConfigs(self):
    configs = db_utils.get_configs()
    if configs:
        response_utils.writeJsonResponse(self, configs)
    else:
        response_utils.InternalServerError(self)