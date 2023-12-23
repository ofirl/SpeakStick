import json
import csv
import io
import os
from zipfile import ZipFile

import utils.db_utils
import utils.response_utils

from common.system_utils import getWordFiles
from common.consts import words_directory


def getLibraries(self, query_parameters, match):
    libraries = utils.db_utils.get_libraries()
    if libraries:
        utils.response_utils.okWithData(self, libraries)
    else:
        utils.response_utils.InternalServerError(self)


def addLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.add_library(name, description)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def duplicateLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.duplicate_library(name, description, match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def editLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")

    success = utils.db_utils.update_library(match.group("id"), name, description)
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def deleteLibrary(self, query_parameters, match):
    success = utils.db_utils.delete_library(match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)


def activateLibrary(self, query_parameters, match):
    success = utils.db_utils.activate_library(match.group("id"))
    if success:
        utils.response_utils.okResponse(self)
    else:
        utils.response_utils.InternalServerError(self)
        
def exportLibrary(self, query_parameters, match):
    libraryId = match.group("id")
    print("library id", libraryId)

    libraryZipContent = io.BytesIO()
    with ZipFile(libraryZipContent, 'w') as zip_file:
        csvFileData = ''
        csvFileData += 'word,positions\n'

        # Add the words files to the zip
        # Add the words data to a csv file
        for libraryId, positions, word in  utils.db_utils.get_library_items(libraryId):
            print("word", word)
            print("positions", positions)
            csvFileData += f'{word},{positions}\n'
            zip_file.write(os.path.join(words_directory, word))
            
        # Add the csv file to the zip
        zip_file.writestr('library.csv', csvFileData)

    # Seek to the beginning of the BytesIO object
    libraryZipContent.seek(0)
    
    utils.response_utils.okWithData(self, libraryZipContent.getvalue())

        
def importLibrary(self, post_data, match):
    json_data = json.loads(post_data.decode("utf-8"))
    name = json_data.get("name")
    description = json_data.get("description")
    libraryZipFile = json_data.get("libraryFile")
    
    zip_file_content_io = io.BytesIO(libraryZipFile)
    success = utils.db_utils.add_library(name, description)
    if success == False:
        utils.response_utils.InternalServerError(self, "error creating new library")
        
    # Where do I get that from??
    libraryId = ''

    # Create a ZipFile object to extract the contents of the zip file
    with ZipFile(zip_file_content_io, 'r') as zip_file:
        # Read the CSV file data
        csvData = zip_file.read('library.csv').decode('utf-8').splitlines()
        csvReader = csv.reader(csvData)
        next(csvReader)  # Skip the header

        for row in csvReader:
            word, positions = row
            
            # Add word to words_directory            
            zip_file.extract(word, words_directory)
            
            # Add library item
            success = utils.db_utils.update_library_item(libraryId, positions, word)
            if success == False:
                utils.response_utils.InternalServerError(self, "error adding word to library")

    utils.response_utils.okResponse(self)
