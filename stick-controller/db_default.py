import sqlite3
import time
import logging

from consts import db_file

defaultConfigs = [
    {
        "key": "STICK_CHECK_INTERVAL_S",
        "value": "0.05",
        "description": "Interval to poll the stick position (in seconds), Recommended to be half the cell change delay (the lower of the 2)",
    },
    {
        "key": "STICK_CHECK_INTERVAL_SLEEP_MODE_S",
        "value": "0.5",
        "description": "Interval to poll the stick position in sleep mode (in seconds)",
    },
    {
        "key": "CELL_CHANGE_DELAY_S",
        "value": "0.2",
        "description": "Delay (in seconds) between the stick changing position and it actually being recorded (usefull for shaky hands)",
    },
    {
        "key": "MIDDLE_CELL_CHANGE_DELAY_S",
        "value": "0.1",
        "description": "Same as `CELL_CHANGE_DELAY_S` only for the middle, this is in a different config because we might want the ability to go over hte middle position quickly",
    },
    {
        "key": "END_WORD_TIMEOUT_S",
        "value": "1",
        "description": "Word will end if no position change is recorded for this duration (in seconds)",
    },
    {
        "key": "SLEEP_TIMEOUT_M",
        "value": "5",
        "description": "How long without an input should the controller wait untill it enters sleep mode (in minutes)",
    },
    {
        "key": "MIDDLE_CELL_OCTAGON_SIDE_LENGTH",
        "value": "0.25",
        "description": "Side length of the center cell octagon (recommended values are 0.15-0.3)",
    },
    {
        "key": "VOLUME",
        "value": "100",
        "description": "Sound volume (values can be 0-100)",
    },
]

advancedConfigs = [
    {
        "key": "ENBALE_AUTOMATIC_UPDATES",
        "value": "1",
        "description": "Enable automatic updates (every day at 1AM)",
    },
    {
        "key": "ENABLE_DEVELOPMENT_BUILDS",
        "value": "0",
        "description": "When updating automatically consider updating to development builds as well",
    },
    {
        "key": "LOGS_API_KEY",
        "value": "",
        "description": "API key for sending logs",
    },
    {
        "key": "DEVICE_NAME",
        "value": "InitialName",
        "description": "Device name for the logs",
    },
    {
        "key": "LOGGING_LEVEL",
        "value": "INFO",
        "description": "Application logging level",
    },
    {
        "key": "LOGS_HANDLER_LOGGING_LEVEL",
        "value": "INFO",
        "description": "Logs handler logging level",
    },
    {
        "key": "LOGGER_API_ENDPOINT",
        "value": "https://log-api.eu.newrelic.com/log/v1",
        "description": "Endpoint to send the logs to",
    },
]

libraries = {
    "Default Library": {
        "description": "Basic library to get started",
        "words": {"8": "Big.wav", "852": "Yes.wav", "456": "No.wav"},
    }
}


def create_default_db(database_file):
    connection = None

    try:
        # Connect to the SQLite database or create it if it doesn't exist
        connection = sqlite3.connect(database_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Create the "configs" table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
                key TEXT PRIMARY KEY,
                value TEXT,
                description TEXT,
                default_value TEXT,
                advanced INTEGER CHECK (advanced IN (0, 1)) DEFAULT 0
            )
        """
        )

        def addConfigToDb(config):
            # Check if the key already exists in the "configs" table
            cursor.execute("SELECT * FROM configs WHERE key = :key", config)
            existing_row = cursor.fetchone()

            if existing_row is None:
                # Insert default values into the "configs" table
                cursor.execute(
                    "INSERT INTO configs (key, value, description, default_value, advanced) VALUES (:key, :value, :description, :value, :advanced)",
                    config,
                )

        for config in defaultConfigs:
            config["advanced"] = "0"
            addConfigToDb(config)

        for config in advancedConfigs:
            config["advanced"] = "1"
            addConfigToDb(config)

        # Create the 'libraries' table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS libraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                active INTEGER CHECK (editable IN (0, 1)),
                editable INTEGER CHECK (editable IN (0, 1))
            )
        """
        )

        # Create the 'library_items' table with a foreign key constraint
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS library_items (
                libraryId INTEGER,
                positions INTEGER,
                word TEXT,
                PRIMARY KEY (libraryId, positions),
                FOREIGN KEY (libraryId) REFERENCES libraries(id) ON DELETE CASCADE
            )
        """
        )

        for libraryName, libraryInfo in libraries.items():
            # Check if the key already exists in the "words" table
            cursor.execute("SELECT * FROM libraries WHERE name = ?", (libraryName,))
            existing_row = cursor.fetchone()

            if existing_row is None:
                # Insert default values into the "words" table
                cursor.execute(
                    "INSERT INTO libraries (name, description, editable, active) VALUES (?, ?, ?, ?)",
                    (libraryName, libraryInfo.get("description"), False, True),
                )

            cursor.execute("SELECT * FROM libraries WHERE name = ?", (libraryName,))
            libraryRow = cursor.fetchone()
            libraryId, _, _, _, _ = libraryRow

            libraryWords = libraryInfo.get("words")
            if libraryWords is None:
                continue

            for positions, word in libraryWords.items():
                cursor.execute(
                    "SELECT * FROM library_items WHERE libraryId = ? AND positions = ?",
                    (libraryId, positions),
                )
                existing_row = cursor.fetchone()

                if existing_row is None:
                    cursor.execute(
                        "INSERT INTO library_items (libraryId, positions, word) VALUES (?, ?, ?)",
                        (libraryId, positions, word),
                    )

        # Commit the changes to the database
        connection.commit()
        logging.info("Default tables and values created successfully")

    except sqlite3.Error as e:
        logging.exception("Error creating default db")

    finally:
        # Close the database connection
        if connection:
            connection.close()


create_default_db(db_file)
