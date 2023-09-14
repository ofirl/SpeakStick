import db_utils
import response_utils

def getLibraries(self, query_parameters):
    libraries = db_utils.get_libraries()
    if libraries:
        response_utils.okWithData(self, libraries)
    else:
        response_utils.InternalServerError(self)