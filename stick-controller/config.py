import sqlite3
from consts import db_file

def read_configs_from_db(database_file):
    configs = {}

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database_file)
        
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

configs = read_configs_from_db(db_file)