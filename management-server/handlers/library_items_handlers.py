import json

import db_utils
import response_utils

def getLibraryItems(self, query_parameters, match_groups):
    libraryId = None
    if query_parameters != None:
        libraryId = query_parameters["libraryId"][0]

    library_items = db_utils.get_library_items(libraryId)
    if library_items != None:
        response_utils.okWithData(self, library_items)
    else:
        response_utils.InternalServerError(self)

def updateLibraryItem(self, post_data, match_groups):
    json_data = json.loads(post_data.decode('utf-8'))
    libraryId = json_data.get('libraryId')
    position = json_data.get('position')
    new_word = json_data.get('word')
    success = db_utils.update_library_item(libraryId, position, new_word)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "error updating position")

def deleteLibraryItem(self, query_parameters, match_groups):
    position = query_parameters.get('position')[0]
    libraryId = query_parameters.get('libraryId')[0]
    if position == None:
        response_utils.BadRequest(self, "Missing required parameter: 'position'")
        return

    success = db_utils.delete_library_item(libraryId, position)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)