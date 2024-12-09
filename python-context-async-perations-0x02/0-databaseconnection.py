#!/usr/bin/python3
import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_values, traceback):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(exc_type, exc_values, traceback)
            return False
           

def query_user():
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

