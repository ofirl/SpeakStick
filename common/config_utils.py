import os
import sqlite3
import logging

from consts import db_file


def get_configs(key=None, advanced=0):
    configs = []
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a query to retrieve data from the "configs" table
        data = {"advanced": str(advanced), "key": key}
        baseQuery = "SELECT * FROM configs WHERE advanced = :advanced"
        if key is not None:
            baseQuery += " AND key = :key"

        cursor.execute(baseQuery, data)

        # Fetch all the rows of data
        rows = cursor.fetchall()

        # Populate the configs dictionary with retrieved data
        for row in rows:
            key, value, description, default_value, _ = row
            configs.append(
                {
                    "key": key,
                    "value": value,
                    "description": description,
                    "default_value": default_value,
                }
            )

    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return configs


def get_config_value(key=None):
    configs = get_configs(key, 1)
    if configs is not None and len(configs) == 1:
        return configs[0]["value"]

    return None


def update_config(key, value):
    output = True
    connection = None

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Update the value in the "configs" table
        cursor.execute(
            "UPDATE configs SET value = :value WHERE key = :key",
            {"value": value, "key": key},
        )
        # Check how many rows were affected by the update
        affected_rows = cursor.rowcount

        # Commit the changes to the database
        connection.commit()

        if affected_rows != 1:
            raise BaseException("Updated ", affected_rows, " rows. Expected 1.")

    except sqlite3.Error as e:
        output = False
        logging.error(f"An error occurred: {e}")

    finally:
        # Close the database connection
        if connection:
            connection.close()

    return output
