#!/usr/bin/env python3

"""
filtered_logger module

This module provides a function to obfuscate sensitive
information in log messages.
"""

import re
from typing import List
import logging
import csv
from logging import StreamHandler
from filtered_logger import RedactingFormatter
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate sensitive information in a log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
            fields in the log line.

    Returns:
        The log message with sensitive information obfuscated.
    """
    return re.sub(r'(?<={}=).*?(?={})'.format('|'.join(fields), separator),
                  redaction, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            log_message,
            self.SEPARATOR
        )


def get_logger():
    """
    Create a logger named "user_data" with StreamHandler
    and RedactingFormatter.

    Returns:
        logging.Logger: The created logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # Creating a StreamHandler
    stream_handler = StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # Adding the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger


# Reading the  user_data.csv to identify PII field
PII_FIELDS = ('field1', 'field2', 'field3', 'field4', 'field5')


def get_db():
    """
    Connect to the MySQL database using credentials from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: The database
        connector object.
    """
    # Get credentials from environment variables
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the database
    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )


if __name__ == "__main__":
    # Connect to the database
    db = get_db()

    # Execute query
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")

    # Print results
    for row in cursor:
        print(row[0])

    # Close cursor and database connection
    cursor.close()
    db.close()


def main():
    """Main function"""
    # Connecting to the database
    db = get_db()
    cursor = db.cursor()

    # Retrieving user data from the database
    cursor.execute("SELECT * FROM users;")
    user_data = cursor.fetchall()

    # Setting up logging
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # Creating a StreamHandler with RedactingFormatter
    stream_handler = StreamHandler()
    stream_handler.setFormatter(RedactingFormatter())

    # Adding the StreamHandler to the logger
    logger.addHandler(stream_handler)

    # Logging user data
    for data in user_data:
        logger.info(f"name={data[0]}; email={data[1]}; phone={data[2]}; "
                    f"ssn={data[3]}; password={data[4]}; ip={data[5]}; "
                    f"last_login={data[6]}; user_agent={data[7]}")

    # Closing cursor and database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
