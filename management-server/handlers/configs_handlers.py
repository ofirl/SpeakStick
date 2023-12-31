import json

import utils.db_utils
import utils.response_utils
import common.config_utils


def getConfigs(self, query_parameters, match):
    advanced = query_parameters.get("advanced")
    if advanced is not None:
        advanced = advanced[0]

    key = query_parameters.get("key")
    if key is not None:
        key = key[0]

    configs = common.config_utils.get_configs(key=key, advanced=advanced)
    if configs:
        utils.response_utils.okWithData(self, configs)
    else:
        utils.response_utils.InternalServerError(self)


def updateConfig(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    key = json_data.get("key")
    value = json_data.get("value")
    success = utils.db_utils.update_config(key, value)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self, "Error updating config")
