#!/usr/bin/python3
import sqlite3

class ExecuteQuery():
    def __init__(self, query, parameter = (25,)):
        """
        Constructor for ExecuteQuery.
        :param query: An SQL query to be executed by the ExecuteQuery object.
        :param parameter: An optional parameter to be passed to the query.
        """
        self.query = query
        self.parameter = parameter

    def __enter__(self):
        """
        Establishes a connection to the SQLite database, executes the query
        that was supplied in the constructor, and returns a cursor object.
        :return: A cursor object pointing to the first entry of the query result.
        """
        self.connection = sqlite3.connect("users.db")
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, self.parameter)
            return self.cursor
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the connection to the SQLite database if it is open, and rolls back
        any uncommitted changes. If an exception occurred during the execution of
        the with block, print the exception and return False.
        :param exc_type: The type of exception that occurred.
        :param exc_value: The value of the exception that occurred.
        :param traceback: The traceback for the exception that occurred.
        :return: False if an exception occurred, otherwise None.
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
            return False

if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM usersm WHERE id < ? ", (5,)) as cursor:
        for row in cursor:
            print(row)