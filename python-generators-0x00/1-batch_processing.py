#!/usr/bin/python3

from mysql.connector import Error
from seed import connect_db

def stream_users_in_batches(batch_size):
    """
    A generator function that yields user data from the user_data table in the ALX_prodev database in batches.

    Args:
        batch_size (int): The number of rows to fetch per batch.

    Yields:
        list: A list of user data dictionaries.
    """
    try:
        with connect_db(database="ALX_prodev") as connection:
            if connection and connection.is_connected():
                with connection.cursor(dictionary=True, buffered=False) as cursor:
                    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
                    while True: 
                        batch = cursor.fetchmany(batch_size)
                        if not batch:
                            break          
                        for row in batch:
                            row["age"] = int(row["age"])
                            yield row
            else:
                raise ValueError("Failed to connect to ALX_prodev database.")

    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

    finally:
        if connection and connection.is_connected():
            connection.close()
# if __name__ == "__main__":
#     batch_size = 10
#     for batch in stream_users_in_batches(batch_size):
#         print(batch)

def batch_processing(batch_size):
    """
    A function that streams user data from the user_data table in the ALX_prodev database in batches.

    Args:
        batch_size (int): The number of rows to fetch per batch.

    Returns:
        None
    """
    for batch in stream_users_in_batches(batch_size):
        if batch["age"] > 25:
            print(batch)

if __name__ == "__main__":
    batch_size = 10
    batch_processing(batch_size)