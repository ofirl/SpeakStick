import db

import response_utils

def getConfigs(self):
    configs = db.get_configs()
    if configs:
        response_utils.writeJsonResponse(self, configs)
    else:
        response_utils.InternalServerError(self)