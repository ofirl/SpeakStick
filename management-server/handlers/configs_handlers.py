import json

import db_utils
import response_utils

def getConfigs(self, query_parameters, match):
    configs = db_utils.get_configs()
    if configs:
        response_utils.okWithData(self, configs)
    else:
        response_utils.InternalServerError(self)

def updateConfig(self, post_data, match):
    json_data = json.loads(post_data.decode('utf-8'))
    key = json_data.get('key')
    value = json_data.get('value')
    success = db_utils.update_config(key, value)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "Error updating config")