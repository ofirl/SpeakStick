import system_utils

import response_utils

def getWords(self):
    positions = system_utils.getWordFiles()
    if positions:
        response_utils.writeJsonResponse(self, positions)
    else:
        response_utils.InternalServerError(self)