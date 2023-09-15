import json

import db_utils
import response_utils

def getLibraries(self, query_parameters):
    libraries = db_utils.get_libraries()
    if libraries:
        response_utils.okWithData(self, libraries)
    else:
        response_utils.InternalServerError(self)

def addLibrary(self, post_data):
    json_data = json.loads(post_data.decode('utf-8'))
    name = json_data.get('name')
    description = json_data.get('description')

    success = db_utils.add_library(name, description)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)

def duplicateLibrary(self, post_data):
    json_data = json.loads(post_data.decode('utf-8'))
    name = json_data.get('name')
    description = json_data.get('description')
    baseLibraryId = json_data.get('baseLibraryId')

    success = db_utils.duplicate_library(name, description, baseLibraryId)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)

def deleteLibrary(self, query_parameters):
    libraryId = query_parameters.get('libraryId')

    success = db_utils.delete_library(libraryId)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self)