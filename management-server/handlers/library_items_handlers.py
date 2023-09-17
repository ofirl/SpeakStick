import json

import utils.db_utils
import utils.response_utils


def getLibraryItems(self, query_parameters, match):
    libraryId = None
    if query_parameters is not None:
        libraryId = query_parameters["libraryId"][0]

    library_items = utils.db_utils.get_library_items(libraryId)
    if library_items is not None:
        utils.response_utils.okWithData(self, library_items)
    else:
        utils.response_utils.InternalServerError(self)


def updateLibraryItem(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    libraryId = json_data.get("libraryId")
    position = json_data.get("position")
    new_word = json_data.get("word")
    success = utils.db_utils.update_library_item(libraryId, position, new_word)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self, "error updating position")


def deleteLibraryItem(self, query_parameters, match):
    position = query_parameters.get("position")[0]
    libraryId = query_parameters.get("libraryId")[0]
    if position is None:
        utils.response_utils.BadRequest(self, "Missing required parameter: 'position'")
        return

    success = utils.db_utils.delete_library_item(libraryId, position)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)
