from flask import Flask, request, redirect, url_for, session, render_template, flash
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'stockflow_key_encrypter'  # Secret key

# Function to validate user credentials
def validate_user(email, password):
    """
    Validate user credentials against the database.
    Returns the user data if valid, otherwise None.
    """
    conn = sqlite3.connect('stockflow.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, name, email, password, account_type FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user[3], password):
        return user
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = validate_user(email, password)

        if user:
            # If match user data from user table
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            session['user_role'] = user[4]

            return redirect(url_for('user_management'))  # Redirect to user management page
        else:
            return render_template('login_page.html', error = "")

    return render_template('login_page.html')

# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    """
    Handle user logout.
    - Clear the session and redirect to the home page.
    """
    session.clear()  # Clear all session data
    return redirect(url_for('home'))  # Redirect to the home page
