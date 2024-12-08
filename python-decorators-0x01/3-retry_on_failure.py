import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to manage database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            print("Database connection established")
            return func(conn, *args, **kwargs)
        except sqlite3.Error as error:
            print("Error while connecting to sqlite:", error)
        finally:
            if conn:
                conn.close()
                print("Database connection closed")
    return wrapper

def retry_on_failure(retries=3, delay=1):
    """
    Decorator to retry a function on failure.
    args:
        retries (int): number of retries
        delay (int): delay between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                     return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts < retries:
                        time.sleep(delay)
                        print(f"attempt {attempts} / {retries} failed: {e} ")
                    else:
                        print("All attempts failed")
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)