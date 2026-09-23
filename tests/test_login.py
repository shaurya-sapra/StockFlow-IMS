import pytest
from test_database import init_test_db
import sys
import os

# Add the project directory for routes.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.routes.routes import app  # Import the Flask app

# Fixture to set up the Flask test client
@pytest.fixture
def client():
    """
    Set up the Flask test client with test configuration and initialise the database with test sample data.
    """
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'  # Use an in-memory database for testing

    with app.test_client() as client:
        with app.app_context():
            init_test_db()  # Initialise the test database
        yield client

def test_failed_login_invalid_credentials(client):
    """
    Test that a user with invalid credentials cannot log in.
    """
    # Simulate a login request with invalid credentials
    response = client.post('/login', data={
        'email': 'admin@stockflow.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    # Verify the response
    assert response.status_code == 200  # Check for a successful response
    assert b'Login' in response.data  # Ensure the user is redirected back to the login page

    with client.session_transaction() as session:
        assert 'user_id' not in session  # Ensure no user_id is set
        assert 'user_email' not in session  # Ensure no user_email is set
