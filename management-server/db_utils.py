import os
import sqlite3

from consts import db_file, words_directory
from system_utils import restartStickController

print("db file:", db_file)

def get_configs():
    configs = []
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Execute a query to retrieve data from the "configs" table
        cursor.execute("SELECT * FROM configs")
        
        # Fetch all the rows of data
        rows = cursor.fetchall()
        
        # Populate the configs dictionary with retrieved data
        for row in rows:
            key, value, description, default_value = row
            configs.append({
                "key": key,
                "value": value,
                "description": description,
                "default_value": default_value
            })
            
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
    
    return configs

def get_library_items(libraryId):
    library_items = []
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Execute a query to retrieve data from the "library_items" table
        if libraryId == None:
            cursor.execute("SELECT * FROM library_items")
        else:
            cursor.execute("SELECT * FROM library_items WHERE libraryId = ?", (libraryId,))
        
        # Fetch all the rows of data
        rows = cursor.fetchall()
        for row in rows:
            libraryId, positions, word = row
            library_items.append({
                "libraryId": libraryId,
                "positions": positions,
                "word": word,
            })
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
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
            libraries.append({
                "id": id,
                "name": name,
                "description": description,
                "active": active == 1,
                "editable": editable == 1,
            })
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
    
    return libraries

def update_config(key, value):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Update the value in the "configs" table
        cursor.execute("UPDATE configs SET value = :value WHERE key = :key", {"value": value, "key": key})        
        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        # Commit the changes to the database
        connection.commit()

        if affected_rows != 1:
            print("Error: Updated ", affected_rows, " rows. Expected 1.")
            output = False
        
        restartStickController()

    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

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

        cursor.execute('SELECT * FROM library_items WHERE libraryId = :libraryId AND positions = :positions', data)
        existing_row = cursor.fetchone()
        
        if existing_row is None:
            cursor.execute('INSERT INTO library_items (libraryId, positions, word) VALUES (:libraryId, :positions, :word)', data)
        else:
            cursor.execute('UPDATE library_items SET word = :word WHERE libraryId = :libraryId AND positions = :positions', data)

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            print("Error: Updated ", affected_rows, " rows. Expected 1.")
            output = False
        else:
            # Commit the changes to the database
            connection.commit()
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output

def add_library(name, description):
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        data = {"name": name, "description": description}

        cursor.execute('SELECT * FROM libraries WHERE name = :name', data)
        existing_row = cursor.fetchone()
        
        if existing_row is not None:
            raise NameError("Library with the name '", name, "' already exists")
        
        cursor.execute('INSERT INTO libraries (name, description, editable, active) VALUES (:name, :description, True, False)', data)

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")
        
        # Commit the changes to the database
        connection.commit()
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

    return True

def duplicate_library(name, description, baseLibraryId):
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        data = {"name": name, "description": description}

        cursor.execute('SELECT * FROM libraries WHERE id = ?', (baseLibraryId,))
        existing_row = cursor.fetchone()
        
        if existing_row is None:
            raise BaseException("Base library with id ", baseLibraryId, " does not exists")
        
        cursor.execute('INSERT INTO libraries (name, description, editable, active) VALUES (:name, :description, True, False)', data)

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")
        
        cursor.execute('SELECT * FROM libraries WHERE name = ?', (name,))
        createdLibrary = cursor.fetchone()
        if createdLibrary is None:
            raise BaseException("Could not find newly created library")

        createdLibraryId, _, _, _, _ = createdLibrary

        baseLibraryItems = get_library_items(baseLibraryId)
        for item in baseLibraryItems:
            # libraryId, positions, word
            cursor.execute('INSERT INTO library_items (libraryId, positions, word) VALUES (:libraryId, :positions, :word)', (createdLibraryId, item.positions, item.word))

            affected_rows = cursor.rowcount
            if affected_rows != 1:
                raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

        # Commit the changes to the database
        connection.commit()
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

    return True

def delete_library_item(libraryId, position):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        cursor.execute('DELETE FROM library_items WHERE libraryId = :libraryId AND positions = :position', {"libraryId": libraryId, "position": position})

        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        # Commit the changes to the database
        connection.commit()

        if affected_rows != 1:
            print("Error: Updated ", affected_rows, " rows. Expected 1.")
            output = False
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
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

        cursor.execute('DELETE FROM library_items WHERE word = ?', (word,))

        # Commit the changes to the database
        connection.commit()

    except sqlite3.Error as e:
        print("An error occurred:", e)
        
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