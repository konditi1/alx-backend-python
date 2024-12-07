#!/usr/bin/python3

from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
import logging
import csv


def connect_db(database=None):
    """
    Establishes a connection to the MySQL database using credentials from the .env file.

    Returns:
        connection: A MySQL connection object if successful, otherwise None.
    """
    load_dotenv()

    try:
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
            )
        
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# if __name__ == "__main__":
#     connection = connect_db()
#     if connection:
#         connection.close()
#         print("Connection closed.")


def create_database(connection):
    """
    Creates the ALX_prodev database if it doesn't exist.

    Args:
        connection: A MySQL connection object.

    Returns:
        None
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")

    except Error as e:
        print(f"Error creating database: {e}")

# if __name__== "__main__":
#     connection = connect_db()
#     if connection:
#         create_database(connection)
#         connection.close()
#         print("Database created.")


def connect_to_prodev():
    """
    Establishes a connection to the ALX_prodev database.

    Returns:
        connection: A MySQL connection object if successful, otherwise None.
    """
    try:
        connection = connect_db(database="ALX_prodev")

        if connection and connection.is_connected():
            # print("Connected to ALX_prodev database.")
            return connection

        else:
            raise ValueError("Failed to connect to ALX_prodev database.")
            
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    

if __name__ == "__main__":
    connection = connect_to_prodev()
    if connection:
        connection.close()
        print("Connection closed.")


def create_table(connection):
    """
    creates a table in the ALX_prodev database.

    Args:
        connection: A MySQL connection object.

    Returns:
        None
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("USE ALX_prodev;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL(3, 0) NOT NULL
                )
            """)
            connection.commit() 
            print("Table user_data created successfully")      

    except Error as e:
        logging.error(f"Error creating table: {e}")
        print(f"Error creating table: {e.errno} - {e.msg}")


# if __name__ == "__main__":
#     connection = connect_to_prodev()
#     if connection:
#         create_table(connection)
#         connection.close()
#         print("Table created.")


def insert_data(connection, data):
    """
    Inserts data into the user_data table in the ALX_prodev database.

    Args:
        connection: A MySQL connection object.
        data: The path to the CSV file containing the data to be inserted.

    Returns:
        None
    """
    try:
        # Validate connection
        if not connection or not connection.is_connected():
            raise ValueError("Invalid or disconnected database connection.")

        with connection.cursor() as cursor:
            cursor.execute("USE ALX_prodev;")

            with open(data, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                required_headers = {"name", "email", "age"}
                if not required_headers.issubset(reader.fieldnames):
                    raise ValueError(f"CSV file is missing required headers: {required_headers - set(reader.fieldnames)}")

                insert_query = """
                    INSERT INTO user_data (name, email, age) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    age = VALUES(age);
                """
                rows_to_insert = []

                for row in reader:
                    name = row["name"].strip()
                    email = row["email"].strip()
                    try:
                        age = int(row["age"])
                    except ValueError:
                        logging.warning(f"Skipping row with invalid age: {row}")
                        continue 

                    rows_to_insert.append((name, email, age))

                if rows_to_insert:
                    cursor.executemany(insert_query, rows_to_insert)
                    connection.commit()
                    # print(f"Inserted {cursor.rowcount} rows successfully.")
                else:
                    print("No valid rows to insert.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {data}")
        logging.error(f"File not found: {e}")

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"Value error: {e}")

    except Error as e:
        print(f"Database error: {e}")
        logging.error(f"Database error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")

# if __name__ == "__main__":
#     connection = connect_to_prodev()
#     if connection:
#         insert_data(connection, 'user_data.csv')
#         connection.close()
#         print("Data inserted.")
#         print("Data insertion task completed.")
     