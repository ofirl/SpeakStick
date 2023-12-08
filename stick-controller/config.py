from common.config_utils import get_configs


def read_configs_from_db():
    configs = {}
    configsList = get_configs(None, 1)
    for config in configsList:
        configs[config["key"]] = config["value"]

    configsList = get_configs(None, 0)
    for config in configsList:
        configs[config["key"]] = config["value"]

    return configs


configs = read_configs_from_db()
