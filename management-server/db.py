import os
import sqlite3

from consts import db_file
print("db file:", db_file)

def get_configs():
    configs = {}

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
            key, value = row
            configs[key] = value
            
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
    
    return configs

def get_positions():
    words = {}

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Execute a query to retrieve data from the "words" table
        cursor.execute("SELECT * FROM words")
        
        # Fetch all the rows of data
        rows = cursor.fetchall()
        
        # Populate the words list with retrieved data
        for row in rows:
            poistions, word = row
            words[poistions] = word
            
        print("words:", words)
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
    
    return words

def update_config(key, value):
    output = True

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Update the value in the "configs" table
        cursor.execute("UPDATE configs SET value = ? WHERE key = ?", (value, key))
        
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

def update_position(position, new_word):
    output = True

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM words WHERE positions = ?', (position))
        existing_row = cursor.fetchone()
        
        if existing_row is None:
            cursor.execute('INSERT INTO words (positions, word) VALUES (?, ?)', (position, new_word))
        else:
            cursor.execute('UPDATE words set word = ?', (new_word))

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

def delete_position(position):
    output = True

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        cursor.execute('DELETE FROM words WHERE positions = ?', (position))

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

def delete_word(word):
    try:
        os.remove(word)
        return None, None
    except FileNotFoundError:
        return "File not found", None
    except Exception as e:
        return "An error occurred", e