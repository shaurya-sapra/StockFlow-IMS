import sqlite3
from werkzeug.security import generate_password_hash

def init_test_db():
    """
    Initialise the test database with test users for authentication tests.
    """
    conn = sqlite3.connect(':memory:')  # Use an in-memory database for testing
    cursor = conn.cursor()

    # Recreate the schema from database.py for the test database
    cursor.executescript('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            account_type TEXT NOT NULL
        );
    ''')

    # Insert test users into the database
    test_users = [
        ('Test Admin', 'admin@stockflow.com', generate_password_hash('admin123'), 'admin'),
        ('Test Employee', 'employee@stockflow.com', generate_password_hash('employee123'), 'employee'),
    ]
    cursor.executemany(
        'INSERT INTO users (name, email, password, account_type) VALUES (?, ?, ?, ?)',
        test_users
    )
    conn.commit()  # Save changes
    conn.close()  # Close the connection
