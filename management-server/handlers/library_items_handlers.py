import json

import db_utils
import response_utils

def getLibraryItems(self, query_parameters):
    libraryId = None
    if query_parameters != None:
        libraryId = query_parameters["libraryId"]

    positions = db_utils.get_library_items(libraryId)
    if positions:
        response_utils.okWithData(self, positions)
    else:
        response_utils.InternalServerError(self)

def updateLibraryItem(self, post_data):
    json_data = json.loads(post_data.decode('utf-8'))
    libraryId = json_data.get('libraryId')
    position = json_data.get('position')
    new_word = json_data.get('word')
    success = db_utils.update_library_item(libraryId, position, new_word)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "error updating position")

def deleteLibraryItem(self, query_parameters):
    position = query_parameters.get('position')
    libraryId = query_parameters.get('libraryId')
    if position == None:
        response_utils.BadRequest(self, "Missing required parameter: 'position'")
        return

    success = db_utils.delete_library_item(libraryId, position)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)