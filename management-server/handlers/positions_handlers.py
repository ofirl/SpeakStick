import json

import db_utils
import response_utils

def getPositions(self):
    positions = db_utils.get_positions()
    if positions:
        response_utils.okWithData(self, positions)
    else:
        response_utils.InternalServerError(self)

def updatePosition(self, post_data):
    json_data = json.loads(post_data.decode('utf-8'))
    position = json_data.get('position')
    new_word = json_data.get('word')
    success = db_utils.update_position(position, new_word)
    if success:
        response_utils.okResponse(self)
    else:
        response_utils.InternalServerError(self, "error updating position")