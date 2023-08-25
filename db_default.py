import os
import sqlite3

SOURCE_DIR = os.path.dirname(__file__)
db_file = SOURCE_DIR + "/configs.db"

defaultConfigs = {
    "SLEEP_DURATION": 0.1, # Define main loop sleep duration
    "CELL_CHANGE_DELAY": 200 # Define cell change delay
}

defaultWords = {
    "8": "applause-1.wav"
}

def create_default_db(database_file):
    try:
        # Connect to the SQLite database or create it if it doesn't exist
        connection = sqlite3.connect(database_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Create the "configs" table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configs (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        for key, value in defaultConfigs.items():
            # Check if the key already exists in the "configs" table
            cursor.execute('SELECT * FROM configs WHERE key = ?', (key,))
            existing_row = cursor.fetchone()
            
            if existing_row is None:
                # Insert default values into the "configs" table
                cursor.execute('INSERT INTO configs (key, value) VALUES (?, ?)', (key, str(value)))
        
        # Create the "words" table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                positions TEXT PRIMARY KEY,
                word TEXT
            )
        ''')

        for posistions, value in defaultWords.items():
            # Check if the key already exists in the "words" table
            cursor.execute('SELECT * FROM words WHERE positions = ?', (key,))
            existing_row = cursor.fetchone()
            
            if existing_row is None:
                # Insert default values into the "words" table
                cursor.execute('INSERT INTO words (positions, word) VALUES (?, ?)', (posistions, str(value)))
        
        # Commit the changes to the database
        connection.commit()
        print("Default tables and values created successfully.")
        
    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    finally:
        # Close the database connection
        if connection:
            connection.close()

create_default_db(db_file)