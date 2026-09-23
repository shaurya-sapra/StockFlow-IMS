from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
from app.database import init_db
from app.routes.login import login, logout
from functools import wraps
from werkzeug.security import generate_password_hash
import sqlite3

# Initialize Flask app with the correct template and static folder paths
app = Flask(__name__,
            template_folder='../../app/templates',  # Path to templates folder
            static_folder='../../app/static')       # Path to static folder

app.secret_key = 'stockflow_secret_session'  # Secret key for session cookie

# Initialise the database
init_db()

# Decorator to ensure only logged-in users can access routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def home():
    return render_template('login_page.html')

# User Management route
@app.route('/user_management')
@login_required
def user_management():
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, name, email, account_type FROM users')
    users = cursor.fetchall()
    conn.close()

    users_list = [
        {'user_id': user[0], 'name': user[1], 'email': user[2], 'account_type': user[3]}
        for user in users
    ]

    return render_template('user_management.html', users=users_list)

# Inventory Tracking route
@app.route('/inventory_tracking')
@login_required
def inventory_tracking():
    return render_template('inventory_tracking.html')

# API: Get all products
@app.route('/api/products')
def get_products():
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.product_id, p.name, p.price, s.stock, c.category_name as category
        FROM products p
        JOIN stock s ON p.product_id = s.product_id
        JOIN categories c ON p.category_id = c.category_id
    ''')
    products = cursor.fetchall()
    conn.close()

    products_list = [
        {
            'product_id': row[0],
            'name': row[1],
            'price': row[2],
            'stock': row[3],
            'category': row[4]
        }
        for row in products
    ]
    return jsonify(products_list)

# API: Update stock for a product
@app.route('/api/update_stock/<int:product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    new_stock = data.get('stock')

    if new_stock is None:
        return jsonify({'error': 'Stock value is required'}), 400

    try:
        new_stock = int(new_stock)  # Ensure stock is an integer
    except (ValueError, TypeError):
        return jsonify({'error': 'Stock value must be an integer'}), 400

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    try:
        # Update the stock in the stock table
        cursor.execute('UPDATE stock SET stock = ? WHERE product_id = ?', (new_stock, product_id))
        conn.commit()

        # Log the stock update in the inventory_log table
        cursor.execute('''
            INSERT INTO inventory_log (product_id, stock_before, stock_after, update_date)
            SELECT ?, stock, ?, DATE('now') FROM stock WHERE product_id = ?
        ''', (product_id, new_stock, product_id))
        conn.commit()

        return jsonify({'success': True}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# API: Get product details
@app.route('/api/product_details/<int:product_id>', methods=['GET'])
@login_required
def get_product_details(product_id):
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    try:
        # Fetch product details
        cursor.execute('''
            SELECT price, weight, calories, carbs, protein, fat, expiry_date, supplier
            FROM products
            WHERE product_id = ?
        ''', (product_id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Match details from product table
        product_details = {
            'price': product[0],
            'weight': product[1],
            'calories': product[2],
            'carbs': product[3],
            'protein': product[4],
            'fat': product[5],
            'expiry_date': product[6],
            'supplier': product[7],
        }
        return jsonify(product_details), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# API: Update product details
@app.route('/api/update_product/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    try:
        # Update the product in the products table
        cursor.execute('''
            UPDATE products
            SET price = ?, weight = ?, calories = ?, carbs = ?, protein = ?, fat = ?, expiry_date = ?, supplier = ?
            WHERE product_id = ?
        ''', (
            data.get('price'),
            data.get('weight'),
            data.get('calories'),
            data.get('carbs'),
            data.get('protein'),
            data.get('fat'),
            data.get('expiry_date'),
            data.get('supplier'),
            product_id
        ))
        conn.commit()

        return jsonify({'success': True}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Product Management route
@app.route('/product_management')
def product_management():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return render_template('privileges_required.html')  # Shows "You do not have privileges" screen

    return render_template('product_management.html')  # Load the product management screen for admins

# API: Add a new product
@app.route('/api/add_product', methods=['POST'])
@login_required
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    try:
        # Insert the new product into the products table
        cursor.execute('''
            INSERT INTO products (category_id, name, price, weight, calories, carbs, protein, fat, expiry_date, supplier)
            VALUES (
                (SELECT category_id FROM categories WHERE category_name = ?),
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ''', (
            data.get('category'),
            data.get('name'),
            data.get('price'),
            data.get('weight'),
            data.get('calories'),
            data.get('carbs'),
            data.get('protein'),
            data.get('fat'),
            data.get('expiry_date'),
            data.get('supplier'),
        ))

        # Get the last inserted product_id
        product_id = cursor.lastrowid

        # Insert the stock data into the stocks table
        cursor.execute('''
            INSERT INTO stock (product_id, stock, last_update)
            VALUES (?, ?, ?)
        ''', (
            product_id,
            data.get('stock'),
            data.get('date_added'),
        ))

        conn.commit()

        return jsonify({'success': True}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# API: Delete a product
@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    try:
        # Delete the product from the products table
        cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))

        # Delete the corresponding stock entry from the stock table
        cursor.execute('DELETE FROM stock WHERE product_id = ?', (product_id,))

        conn.commit()

        return jsonify({'success': True}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Inventory Reporting route
@app.route('/inventory_reporting')
@login_required
def inventory_reporting():
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    # Fetch total products
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    # Fetch total stock
    cursor.execute('SELECT SUM(stock) FROM stock')
    total_stock = cursor.fetchone()[0]

    # Fetch category distribution
    cursor.execute('''
        SELECT c.category_name, COUNT(p.product_id) 
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_name
    ''')
    category_distribution = cursor.fetchall()
    categories = [row[0] for row in category_distribution]
    counts = [row[1] for row in category_distribution]

    # Fetch stock history
    cursor.execute('''
        SELECT update_date, SUM(stock_after) 
        FROM inventory_log
        GROUP BY update_date
        ORDER BY update_date
    ''')
    stock_history = cursor.fetchall()
    dates = [row[0] for row in stock_history]
    stock = [row[1] for row in stock_history]

    conn.close()

    return render_template('inventory_reporting.html',
                           total_products=total_products,
                           total_stock=total_stock,
                           categories=categories,
                           counts=counts,
                           dates=dates,
                           stock=stock)

# API: Get category distribution
@app.route('/api/category_distribution')
def category_distribution():
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    # Fetch category distribution
    cursor.execute('''
        SELECT c.category_name, COUNT(p.product_id) 
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_name
    ''')
    category_distribution = cursor.fetchall()
    conn.close()

    # Format data for JSON response
    categories = [row[0] for row in category_distribution]
    counts = [row[1] for row in category_distribution]

    return jsonify({
        "categories": categories,
        "counts": counts
    })

# API: Get stock history
@app.route('/api/stock_history')
def stock_history():
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()

    # Fetch stock history
    cursor.execute('''
        SELECT update_date, SUM(stock_after) 
        FROM inventory_log
        GROUP BY update_date
        ORDER BY update_date
    ''')
    stock_history = cursor.fetchall()
    conn.close()

    # Format data for JSON response
    dates = [row[0] for row in stock_history]
    stock = [row[1] for row in stock_history]

    return jsonify({
        "dates": dates,
        "stock": stock
    })

# Promote user to admin
@app.route('/promote/<int:user_id>', methods=['POST'])
@login_required
def promote(user_id):
    if session.get('user_role') != 'admin':
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('user_management'))

    if session.get('user_id') == user_id:
        flash('You cannot change your own permissions!', 'error')
        return redirect(url_for('user_management'))

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET account_type = "admin" WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User promoted to admin successfully!', 'success')
    return redirect(url_for('user_management'))

# Demote user to employee
@app.route('/demote/<int:user_id>', methods=['POST'])
@login_required
def demote(user_id):
    if session.get('user_role') != 'admin':
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('user_management'))

    if session.get('user_id') == user_id:
        flash('You cannot change your own permissions!', 'error')
        return redirect(url_for('user_management'))

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET account_type = "employee" WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User demoted to employee successfully!', 'success')
    return redirect(url_for('user_management'))

# Delete user
@app.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if session.get('user_role') != 'admin':
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('user_management'))

    if session.get('user_id') == user_id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('user_management'))

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('user_management'))

# Add a new user
@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if session.get('user_role') != 'admin':
        flash("You do not have permission to add users.", "error")
        return redirect(url_for('user_management'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    account_type = request.form.get('account_type')

    if not name or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for('user_management'))

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password, account_type) VALUES (?, ?, ?, ?)",
                       (name, email, hashed_password, account_type))
        conn.commit()
        flash("User added successfully!", "success")
    except sqlite3.IntegrityError:
        flash("Email already exists.", "error")
    finally:
        conn.close()

    return redirect(url_for('user_management'))  # Redirect instead of returning JSON

# Register authentication routes
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET'])