import json

import utils.versions_utils
import utils.response_utils


def getApplicationVersions(self, query_parameters, match):
    versions = utils.versions_utils.get_versions()
    if versions is not None:
        utils.response_utils.okWithData(self, versions)
    else:
        utils.response_utils.InternalServerError(
            self, "Error getting application versions"
        )


def getApplicationCurrentVersion(self, query_parameters, match):
    version = utils.versions_utils.get_current_version()
    if version is not None:
        utils.response_utils.okWithData(self, version)
    else:
        utils.response_utils.InternalServerError(
            self, "Error getting application current version"
        )


def switchApplicationVersion(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    version = json_data.get("version")

    success = utils.versions_utils.switch_version(version)
    if success is not None:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(
            self, "Error switching application versions"
        )


def updateApplicationVersions(self, query_parameters, match):
    success = utils.versions_utils.update_available_versions()
    if success is not None:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(
            self, "Error updating application versions"
        )


def getChageLog(self, query_parameters, match):
    changeLog = utils.versions_utils.get_github_releases()
    if changeLog is not None:
        utils.response_utils.okWithData(self, changeLog)
    else:
        utils.response_utils.InternalServerError(self, "Error getting change log")
