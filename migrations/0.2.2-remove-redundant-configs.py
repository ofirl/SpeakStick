import sqlite3

# Define the migration version
version = "0.2.2"

from consts import db_file


def migrate():
    connection = sqlite3.connect(db_file)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Create the "configs" table if it doesn't exist
    cursor.execute(
        """
        DELETE FROM configs WHERE key = 'LAST_LOG_SAMPLE'
        """
    )
