import sqlite3
from consts import db_file


def get_word_by_position(positions):
    connection = None
    word = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to retrieve the row with the specified position
        cursor.execute(
            "SELECT word FROM library_items WHERE libraryId in (SELECT id FROM libraries WHERE active = True) AND positions = ?",
            (positions,),
        )

        # Fetch the row data
        row = cursor.fetchone()

        print("row")
        print(row)
        # If a row was found, extract the word
        if row:
            word = row

    except sqlite3.Error as e:
        print("An error occurred:", e)

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return word
