#!/usr/bin/python3

import sqlite3
import csv
import uuid
import logging
import traceback
import re

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
def create_user_table():
    """
    Creates the users table
    """
    try:
        with sqlite3.connect('users.db') as connection:
            cursor = connection.cursor()
            user_schema = """ CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
            cursor.execute(user_schema)
            connection.commit()
            print("User table created successfully")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)


def insert_data(data):
    """
    Inserts dat Into the users table from a csv file
    """
    try:
        with sqlite3.connect('users.db') as connection:
            cursor = connection.cursor()
            with open(data, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                required_fields = { 'name', 'email', 'age'}
                if not reader.fieldnames:
                    raise ValueError("The CSV file is empty or missing a header row.")
                if not required_fields.issubset(reader.fieldnames):
                    raise ValueError("Missing required fields in the CSV file")

                insert_query = """INSERT INTO users(user_id, name, email, age)
                    VALUES(?, ?, ?, ?)
                    ON CONFLICT(email) DO UPDATE SET
                        name = excluded.name,
                        email = excluded.email,
                        age = excluded.age
                """
                
                for row in reader:
                    user_id = row.get('user_id') or str(uuid.uuid4())
                    name = row['name'].strip()
                    email = row['email'].strip()
                    age = row.get('age')
                    if not age or not age.isdigit():                   
                        logging.error("Skipping row due to Invalid age value: %s", row['age'])
                        continue
                    age = float(age)

                    cursor.execute(insert_query, (user_id, name, email, age))
                connection.commit()
                print("Data inserted successfully")

    except FileNotFoundError as e:
        print(f"Error: File not found - {data}")
        logging.error(f"File not found: {e}")

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"Value error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")            
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

if __name__ == "__main__":
    insert_data('users.csv')
                        
                