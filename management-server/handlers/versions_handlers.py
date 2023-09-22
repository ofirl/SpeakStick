import utils.versions_utils
import utils.response_utils


def performUpgrade(self, query_parameters, match):
    version = query_parameters.get("version")
    if version is not None:
        version = version[0]

    process, err = utils.versions_utils.runUpgrade(version)
    if err is None and process is not None:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def isUpgradeRunning(self, query_parameters, match):
    isRunning = utils.versions_utils.isUpgradeRunning()
    if isRunning is not None:
        utils.response_utils.okWithData(self, isRunning)
    else:
        utils.response_utils.InternalServerError(self)


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


def updateApplicationVersions(self, query_parameters, match):
    success = utils.versions_utils.update_available_versions()
    if success is not None:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(
            self, "Error updating application versions"
        )


def getChageLog(self, query_parameters, match):
    changeLog, error = utils.versions_utils.get_github_releases()
    if changeLog is not None:
        utils.response_utils.okWithData(self, changeLog)
    else:
        utils.response_utils.InternalServerError(
            self, f"Error getting change log, {error}"
        )
