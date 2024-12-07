import sqlite3
import functools
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename='0-log_queries.log', filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s')

#### decorator to log SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{datetime.now()} - Executing query: {kwargs.get('query')}")
        logging.info(f"Executing query: {kwargs.get('query')}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")