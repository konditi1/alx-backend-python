#!/usr/bin/python3

from seed import connect_to_prodev
from mysql.connector import Error

def stream_user_ages():
    """
    A generator function that yields user ages from the user_data table in the ALX_prodev database.
    """
    try:
        with connect_to_prodev() as connection:
            if connection and connection.is_connected():
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT age FROM user_data;")
                    for row in cursor:
                        yield row['age']
            else:
                raise ValueError("Failed to connect to ALX_prodev database.")

    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    
    finally:
        if connection and connection.is_connected():
            connection.close()
            # print("Connection closed.")


def average_user_age():
    """
    Calculates the average user age from the user_data table in the ALX_prodev database.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count <= 0:
        return None
    return f"Average age of users: {total / count}"


if __name__ == "__main__":
    for age in stream_user_ages():
        print(age)
    print(average_user_age())

