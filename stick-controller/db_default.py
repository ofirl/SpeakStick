import sqlite3

from consts import db_file

defaultConfigs = [
    {
        "key": "SLEEP_DURATION_S",
        "value": "0.1",
        "description": "Interval to poll the stick position, Recommended to be half the cell change delay (the lower of the 2)"
    },
    {
        "key": "CELL_CHANGE_DELAY_S",
        "value": "0.2",
        "description": "Delay between the stick changing position and it actually being recorded (usefull for shaky hands)"
    },
    {
        "key": "MIDDLE_CELL_CHANGE_DELAY_S",
        "value": "0.1",
        "description": "Same as `CELL_CHANGE_DELAY_S` only for the middle, this is in a different config because we might want the ability to go over hte middle position quickly"
    },
    {
        "key": "END_WORD_TIMEOUT_S",
        "value": "1",
        "description": "Word will end if no position change is recorded for this duration"
    }
]

defaultWords = {
    "8": "applause-1.wav"
}

def create_default_db(database_file):
    connection = None
    
    try:
        # Connect to the SQLite database or create it if it doesn't exist
        connection = sqlite3.connect(database_file)
        
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Create the "configs" table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configs (
                key TEXT PRIMARY KEY,
                value TEXT,
                description TEXT,
                default_value TEXT
            )
        ''')
        
        for config in defaultConfigs:
            print(config)
            # Check if the key already exists in the "configs" table
            cursor.execute('SELECT * FROM configs WHERE key = :key', config)
            existing_row = cursor.fetchone()
            
            if existing_row is None:
                # Insert default values into the "configs" table
                cursor.execute('INSERT INTO configs (key, value, description, default_value) VALUES (:key, :value, :description, :value)', config)
        
        # Create the "words" table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                positions TEXT PRIMARY KEY,
                word TEXT
            )
        ''')

        for posistions, value in defaultWords.items():
            # Check if the key already exists in the "words" table
            cursor.execute('SELECT * FROM words WHERE positions = ?', (posistions,))
            existing_row = cursor.fetchone()
            
            if existing_row is None:
                # Insert default values into the "words" table
                cursor.execute('INSERT INTO words (positions, word) VALUES (?, ?)', (posistions, value))
        
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