import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            conn = sqlite3.connect('users.db')
            with conn:
                return func(conn, *args, **kwargs)
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if conn:
                conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, age): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE age = ?", (age,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(age=1)
print(user)