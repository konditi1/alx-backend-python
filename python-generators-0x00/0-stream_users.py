#!/usr/bin/python3

from mysql.connector import Error

seed = __import__('seed')

def stream_users():
    """
    A generator function that yields user data from the user_data table in the ALX_prodev database.
    """ 
    try:
        with seed.connect_to_prodev() as connection:
            if connection and connection.is_connected():
                with connection.cursor(dictionary=True, buffered=True) as cursor:
                        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
                        
                        for row in cursor:
                            yield { f"user_id: {row['user_id']}, name: {row['name']}, email: {row['email']}, age: {row['age']}" }                   
                        
            else:
                raise ValueError("Failed to connect to ALX_prodev database.")
    
    except TypeError as e:
            print(f"Error connecting to ALX_prodev: {e}")
            return None

    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()
            # print("Connection closed.")
# if __name__ == "__main__":
#     for row in stream_users():
#         print(row)
