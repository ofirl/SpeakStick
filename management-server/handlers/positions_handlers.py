import db

import response_utils

def getPositions(self):
    positions = db.get_positions()
    if positions:
        response_utils.writeJsonResponse(self, positions)
    else:
        response_utils.InternalServerError(self)