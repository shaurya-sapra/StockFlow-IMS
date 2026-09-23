import sqlite3
from werkzeug.security import generate_password_hash

# Create stockflow database
def connect_db():
    return sqlite3.connect('stockflow.db')

def create_table(cursor, query):
    cursor.execute(query)

def insert_data(cursor, query, data):
    cursor.executemany(query, data)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create tables
    tables = {
        "users": '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                account_type TEXT NOT NULL
            )
        ''',
        "categories": '''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        ''',
        "products": '''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                weight REAL NOT NULL,
                calories INTEGER NOT NULL,
                carbs REAL NOT NULL,
                protein REAL NOT NULL,
                fat REAL NOT NULL,
                expiry_date TEXT NOT NULL,
                supplier TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        ''',
        "stock": '''
            CREATE TABLE IF NOT EXISTS stock (
                product_id INTEGER PRIMARY KEY,
                stock INTEGER NOT NULL,
                last_update TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''',
        "inventory_log": '''
            CREATE TABLE IF NOT EXISTS inventory_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                stock_before INTEGER NOT NULL,
                stock_after INTEGER NOT NULL,
                update_date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        '''
    }

    for query in tables.values():
        create_table(cursor, query)

    # Insert sample data
    sample_users = [
        ('Tester One', 'tester1@stockflow.com', generate_password_hash('tester1password'), 'admin'),
        ('Tester Two', 'tester2@stockflow.com', generate_password_hash('tester2password'), 'admin'),
        ('Tester Three', 'tester3@stockflow.com', generate_password_hash('tester3password'), 'employee'),
        ('Tester Four', 'tester4@stockflow.com', generate_password_hash('tester4password'), 'employee'),
        ('Tester Five', 'tester5@stockflow.com', generate_password_hash('tester5password'), 'employee'),
    ]
    insert_data(cursor, 'INSERT OR IGNORE INTO users (name, email, password, account_type) VALUES (?, ?, ?, ?)',
                sample_users)

    sample_categories = [
        ('Fruit & Veg', 'Fresh fruits and vegetables'),
        ('Dairy', 'Milk, cheese, yogurt and more'),
        ('Meat', 'Various meat products'),
        ('Snacks', 'Chips, crisps, pretzels, and more'),
        ('Bread & Bakery', 'Bread, pastries, and bakery items')
    ]
    insert_data(cursor, 'INSERT OR IGNORE INTO categories (category_name, description) VALUES (?, ?)',
                sample_categories)

    # Mapping dictionary: category name -> category_id
    category_mapping = {
        'Fruit & Veg': 1,
        'Dairy': 2,
        'Meat': 3,
        'Snacks': 4,
        'Bread & Bakery': 5
    }

    # Insert products
    products = [
        ('Orange', 'Fruit & Veg', 0.99, 150, 41, 8.2, 0.8, 0.2, '2025-03-07', 'SUPPLIER3'),
        ('Mango', 'Fruit & Veg', 0.95, 140, 56, 10.7, 0.7, 0.6, '2025-02-28', 'SUPPLIER1'),
        ('Cucumber', 'Fruit & Veg', 0.79, 158, 16, 1.2, 1.0, 0.6, '2025-03-03', 'SUPPLIER1'),
        ('Milk', 'Dairy', 1.45, 568, 100, 9.6, 7.2, 2.2, '2025-02-27', 'SUPPLIER2'),
        ('Cheese', 'Dairy', 3.20, 119, 125, 0.1, 7.6, 10.5, '2025-02-28', 'SUPPLIER3'),
        ('Eggs', 'Dairy', 1.95, 276, 79, 0.1, 7.6, 5.4, '2025-03-01', 'SUPPLIER2'),
        ('Chicken', 'Meat', 6.20, 200, 154, 0.1, 34.8, 1.6, '2025-03-07', 'SUPPLIER1'),
        ('Lamb', 'Meat', 6.00, 800, 232, 1.8, 22.3, 15.0, '2025-03-10', 'SUPPLIER1'),
        ('Duck', 'Meat', 4.80, 397, 263, 0.1, 16, 22, '2025-03-01', 'SUPPLIER2'),
        ('Popcorn', 'Snacks', 0.99, 180, 110, 10.2, 1.6, 6.6, '2025-03-15', 'SUPPLIER3'),
        ('Crisps', 'Snacks', 2.50, 185, 144, 18.0, 1.8, 6.6, '2025-03-20', 'SUPPLIER2'),
        ('Pretzels', 'Snacks', 1.50, 143, 118, 23.0, 3.0, 1.4, '2025-03-25', 'SUPPLIER2'),
        ('Bread', 'Bread & Bakery', 1.39, 800, 93, 17.9, 3.5, 0.7, '2025-03-03', 'SUPPLIER3'),
    ]

    product_data = [(category_mapping[cat], name, price, weight, calories, carbs, protein, fat, expiry_date, supplier)
                    for name, cat, price, weight, calories, carbs, protein, fat, expiry_date, supplier in products]
    insert_data(cursor, '''
        INSERT OR IGNORE INTO products (category_id, name, price, weight, calories, carbs, protein, fat, expiry_date, supplier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', product_data)

    # Insert stock data
    stock_data = [
        (1, 22, '2025-02-20'), (2, 69, '2025-02-25'), (3, 92, '2025-02-20'),
        (4, 52, '2025-02-23'), (5, 88, '2025-02-22'), (6, 8, '2025-02-28'),
        (7, 76, '2025-02-25'), (8, 24, '2025-02-26'), (9, 8, '2025-02-26'),
        (10, 24, '2025-02-27'), (11, 56, '2025-02-23'), (12, 69, '2025-02-25'),
        (13, 35, '2025-03-01'), (14, 48, '2025-02-24'), (15, 87, '2025-02-25'),
    ]

    insert_data(cursor, 'INSERT OR IGNORE INTO stock (product_id, stock, last_update) VALUES (?, ?, ?)', stock_data)

    # Insert inventory log data
    inventory_logs = [
        (1, 55, 49, '2025-02-22'), (1, 49, 45, '2025-02-25'), (1, 45, 41, '2025-02-27'),
        (2, 60, 53, '2025-02-21'), (2, 53, 47, '2025-02-24'), (2, 47, 42, '2025-02-28'),
        (3, 70, 65, '2025-02-22'), (3, 65, 60, '2025-02-26'), (3, 60, 55, '2025-03-01'),
    ]

    insert_data(cursor,
                'INSERT INTO inventory_log (product_id, stock_before, stock_after, update_date) VALUES (?, ?, ?, ?)',
                inventory_logs)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
