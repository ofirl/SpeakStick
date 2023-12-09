import json

import utils.db_utils
import utils.response_utils


def getLibraries(self, query_parameters, match):
    libraries = utils.db_utils.get_libraries()
    if libraries:
        utils.response_utils.okWithData(self, libraries)
    else:
        utils.response_utils.InternalServerError(self)


def addLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.add_library(name, description)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)
        
def importLibrary(self, post_data, match):
    success = True


def duplicateLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.duplicate_library(name, description, match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def editLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.update_library(match.group("id"), name, description)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def deleteLibrary(self, query_parameters, match):
    success = utils.db_utils.delete_library(match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def activateLibrary(self, query_parameters, match):
    success = utils.db_utils.activate_library(match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)
        
def exportLibrary(self, query_parameters, match):
    success = True
