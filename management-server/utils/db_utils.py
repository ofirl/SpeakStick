import os
import sqlite3
import logging

import common.config_utils

from common.consts import db_file, words_directory
from common.system_utils import restartStickController

logging.debug("db file: ${db_file}")


def get_library_items(libraryId):
    library_items = []
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to retrieve data from the "library_items" table
        if libraryId is None:
            cursor.execute("SELECT * FROM library_items")
        else:
            cursor.execute(
                "SELECT * FROM library_items WHERE libraryId = ?", (libraryId,)
            )

        # Fetch all the rows of data
        rows = cursor.fetchall()
        for row in rows:
            libraryId, positions, word = row
            library_items.append(
                {
                    "libraryId": libraryId,
                    "positions": positions,
                    "word": word,
                }
            )

    except sqlite3.Error as e:
        logging.exception(f"Error get library items", extra={"libraryId": libraryId})

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return library_items


def get_libraries():
    libraries = []
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to retrieve data from the "libraries" table
        cursor.execute("SELECT * FROM libraries")

        # Fetch all the rows of data
        rows = cursor.fetchall()

        for row in rows:
            id, name, description, active, editable = row
            libraries.append(
                {
                    "id": id,
                    "name": name,
                    "description": description,
                    "active": active == 1,
                    "editable": editable == 1,
                }
            )

    except sqlite3.Error as e:
        logging.exception(f"Error getting libraries")

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return libraries


def get_library_by_id(libraryId):
    library = None
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to retrieve data from the "libraries" table
        cursor.execute("SELECT * FROM libraries where id = ?", (libraryId,))

        # Fetch all the rows of data
        libraryRow = cursor.fetchone()

        if libraryRow is None:
            raise BaseException("Could not find library with ID ", libraryId)

        id, name, description, active, editable = libraryRow

        library = {
            "id": id,
            "name": name,
            "description": description,
            "active": active == 1,
            "editable": editable == 1,
        }

    except sqlite3.Error as e:
        logging.exception(f"Error getting library", extra={"libraryId": libraryId})

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return library


def update_config(key, value, restart=True):
    output = common.config_utils.update_config(key, value)
    if output == True and restart:
        restartStickController()

    return output


def update_library_item(libraryId, positions, new_word):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        data = {"libraryId": libraryId, "positions": positions, "word": new_word}

        cursor.execute(
            "SELECT * FROM library_items WHERE libraryId = :libraryId AND positions = :positions",
            data,
        )
        existing_row = cursor.fetchone()

        if existing_row is None:
            cursor.execute(
                "INSERT INTO library_items (libraryId, positions, word) VALUES (:libraryId, :positions, :word)",
                data,
            )
        else:
            cursor.execute(
                "UPDATE library_items SET word = :word WHERE libraryId = :libraryId AND positions = :positions",
                data,
            )

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")
        else:
            # Commit the changes to the database
            connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(
            f"Error updating library item",
            extra={"libraryId": libraryId, "positions": positions, "word": new_word},
        )

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def add_library(name, description):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        data = {"name": name, "description": description}

        cursor.execute("SELECT * FROM libraries WHERE name = :name", data)
        existing_row = cursor.fetchone()

        if existing_row is not None:
            raise NameError("Library with the name '", name, "' already exists")

        cursor.execute(
            "INSERT INTO libraries (name, description, editable, active) VALUES (:name, :description, True, False)",
            data,
        )

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(f"Error adding library", extra={"name": name})

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def update_library(libraryId, name, description):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        data = {"id": libraryId, "name": name, "description": description}

        library = get_library_by_id(libraryId)
        if library is None:
            raise NameError("Library with the ID '", libraryId, "' does not exists")
        if library.get("editable") == 0:
            raise NameError("Library with the ID '", libraryId, "' is not editable")

        cursor.execute(
            "UPDATE libraries SET name = :name, description = :description WHERE id = :id",
            data,
        )

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(
            f"Error updating library",
            extra={"libraryId": libraryId, "name": name, "description": description},
        )

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def duplicate_library(name, description, baseLibraryId):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        data = {"name": name, "description": description}

        cursor.execute("SELECT * FROM libraries WHERE id = ?", (baseLibraryId,))
        existing_row = cursor.fetchone()

        if existing_row is None:
            raise BaseException(
                "Base library with id ", baseLibraryId, " does not exists"
            )

        cursor.execute(
            "INSERT INTO libraries (name, description, editable, active) VALUES (:name, :description, True, False)",
            data,
        )

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        cursor.execute("SELECT * FROM libraries WHERE name = ?", (name,))
        createdLibrary = cursor.fetchone()
        if createdLibrary is None:
            raise BaseException("Could not find newly created library")

        createdLibraryId, _, _, _, _ = createdLibrary

        baseLibraryItems = get_library_items(baseLibraryId)
        for item in baseLibraryItems:
            cursor.execute(
                "INSERT INTO library_items (libraryId, positions, word) VALUES (:libraryId, :positions, :word)",
                (createdLibraryId, item.get("positions"), item.get("word")),
            )

            affected_rows = cursor.rowcount
            if affected_rows != 1:
                raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(
            f"Error duplicating library",
            extra={
                "baseLibraryId": baseLibraryId,
                "name": name,
                "description": description,
            },
        )

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def delete_library_item(libraryId, position):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM library_items WHERE libraryId = :libraryId AND positions = :position",
            {"libraryId": libraryId, "position": position},
        )

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        # Commit the changes to the database
        connection.commit()

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

    except sqlite3.Error as e:
        output = False
        logging.exception(
            f"Error deleting library item",
            extra={"libraryId": libraryId, "position": position},
        )

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def delete_library(libraryId):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        library = get_library_by_id(libraryId)
        if library is None:
            raise BaseException("Could not get library with ID ", libraryId)

        if library.get("editable") == False or library.get("active") == True:
            raise BaseException("Can't delete locked or active library")

        cursor.execute("DELETE FROM libraries WHERE id = ?", (libraryId,))

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        cursor.execute("DELETE FROM library_items WHERE libraryId = ?", (libraryId,))

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(f"Error deleting library", extra={"libraryId": libraryId})

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def delete_library_items_for_word(word):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        cursor.execute("DELETE FROM library_items WHERE word = ?", (word,))

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(
            f"Error deleting library items for word", extra={"word": word}
        )

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output


def delete_word(word):
    try:
        os.remove(os.path.join(words_directory, "".join(word)))

        if not delete_library_items_for_word(word):
            return Exception.__init__("Error deleting positions for word " + word)

        return None

    except Exception as e:
        return e


def activate_library(
    libraryId,
):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        cursor.execute("UPDATE libraries SET active = False WHERE active = True")
        affected_rows = cursor.rowcount
        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        cursor.execute("UPDATE libraries SET active = True WHERE id = ?", (libraryId,))
        affected_rows = cursor.rowcount
        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        output = False
        logging.exception(f"Error activating library", extra={"libraryId": libraryId})

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output
