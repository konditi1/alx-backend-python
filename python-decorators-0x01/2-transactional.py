import sqlite3
import functools

def with_db_connection(func):
    """Decorator to manage database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')  # Establish connection
            print("Database connection established")
            return func(conn, *args, **kwargs)  # Pass connection to the function
        except sqlite3.Error as error:
            print("Error while connecting to sqlite:", error)
        finally:
            if conn:
                conn.close()  # Ensure connection is closed
                print("Database connection closed")
    return wrapper

def transactional(func):
    """Decorator to manage transactions within an existing connection."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            with conn:  # Handle transactions automatically
                result = func(conn, *args, **kwargs)
                print("Transaction committed successfully")
                return result
        except sqlite3.Error as error:
            print("Error during transaction:", error)
            conn.rollback()
            print("Transaction rolled back")
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email): 
    """Update the email of a user in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Email updated for user_id {user_id} to {new_email}")

if __name__ == "__main__":
    # Update a user's email
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
