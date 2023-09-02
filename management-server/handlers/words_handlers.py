import os

import system_utils
import response_utils
import db_utils

from consts import words_directory
from urllib.parse import parse_qs

def getWords(self):
    positions = system_utils.getWordFiles()
    if positions:
        response_utils.okWithData(self, positions)
    else:
        response_utils.InternalServerError(self)

def updateWord(self, post_data):
    file_name = self.headers.get('filename', '')
    if file_name == "":
        response_utils.BadRequest(self, "Mssing 'filename' header")
        return

    file_path = os.path.join(words_directory, file_name)

    with open(file_path, 'wb') as f:
        f.write(post_data)

    response_utils.okWithText(self, f"File '{file_name}' uploaded successfully" )

def deleteWord(self):
    query_parameters = parse_qs(self.path.split('?')[1])
    word = query_parameters.get('word')
    if not word:
        response_utils.BadRequest(self, "Missing required parameter: 'word'")
        return

    error = db_utils.delete_word("".join(word))
    if error == None:
        response_utils.okResponse(self)
    else:
        print(error.__str__().encode())
        response_utils.InternalServerError(self, "Error deleting word")