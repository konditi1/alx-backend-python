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
query_cache = {}

def cache_query(func):
    """
    Decorator to cache query results for a specified timeout.
    Args:
        timeout (int): The number of seconds to cache the query result.

    Note:
        The decorated function must accept a 'query' keyword argument.
    """
    timeout = 10
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')

        if not query:
            raise ValueError("A valid 'query' must be provided in kwargs")

        if query in query_cache:
            cached_result, query_sent_time = query_cache[query]
            if time.time() - query_sent_time < timeout:
                print("Cache hit")
                return cached_result
            else:
                print("Cache expired")

        result = func(*args, **kwargs)
        query_cache[query] = (result, time.time())
        print("Cache updated")
        return result

    return wrapper




@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")