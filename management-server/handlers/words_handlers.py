import os
import urllib.parse

import utils.system_utils
import utils.response_utils
import utils.db_utils

from consts import words_directory
from urllib.parse import parse_qs


def getWords(self, query_parameters, match):
    positions = utils.system_utils.getWordFiles()
    if positions:
        utils.response_utils.okWithData(self, positions)
    else:
        utils.response_utils.InternalServerError(self)


def updateWord(self, post_data, match):
    file_name = urllib.parse.unquote(self.headers.get("filename", ""))
    if file_name == "":
        utils.response_utils.BadRequest(self, "Mssing 'filename' header")
        return

    file_path = os.path.join(words_directory, file_name)

    with open(file_path, "wb") as f:
        f.write(post_data)

    utils.response_utils.okWithText(self, f"File '{file_name}' uploaded successfully")


def deleteWord(self, query_parameters, match):
    word = query_parameters.get("word")
    if not word:
        utils.response_utils.BadRequest(self, "Missing required parameter: 'word'")
        return

    error = utils.db_utils.delete_word("".join(word))
    if error is None:
        utils.response_utils.okResponse(self)
    else:
        print(error.__str__().encode())
        utils.response_utils.InternalServerError(self, "Error deleting word")
