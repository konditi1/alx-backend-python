#!/usr/bin/python3
import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        """
        Constructor for DatabaseConnection.        
        :param db_name: The name of the database to be connected to.
        """
        
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Establishes a connection to the SQLite database.
        :return: A connection object pointing to the database.
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_values, traceback):
        """
        Closes the connection to the SQLite database if it is open, and rolls back
        any uncommitted changes. If an exception occurred during the execution of
        the with block, print the exception and return False.
        :param exc_type: The type of exception that occurred.
        :param exc_values: The value of the exception that occurred.
        :param traceback: The traceback for the exception that occurred.
        :return: False if an exception occurred, otherwise None.
        """
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(exc_type, exc_values, traceback)
            return False
           

def query_user():
    """
    Queries the users.db database and prints all entries in the users table.
    If an exception occurs, the exception is printed.
    """
    with DatabaseConnection("users.db") as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            for row in cursor:
                print(row)
                # yield row
        except Exception as e:
            print(e)


if __name__ == "__main__":
    query_user()

