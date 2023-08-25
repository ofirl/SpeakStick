import sqlite3

from consts import db_file
print("db file:", db_file)
# print(db_file)

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

def get_words():
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
            
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()
    
    return words

def update_config(key, value):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Update the value in the "configs" table
        cursor.execute("UPDATE configs SET value = ? WHERE key = ?", (value, key))
        
        # Commit the changes to the database
        connection.commit()
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

    return True

def update_word(position, new_word):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Update the word in the "words" table
        cursor.execute("UPDATE words SET word = ? WHERE positions = ?", (new_word, position))
        
        # Commit the changes to the database
        connection.commit()
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

    return True