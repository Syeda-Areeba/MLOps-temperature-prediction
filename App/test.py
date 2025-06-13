import pytest
from flask import Flask
from flask.testing import FlaskClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  

@pytest.fixture
def client() -> FlaskClient:
    # Create a test client for the Flask app
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    yield app.test_client()  # Provides a test client
    # Teardown if needed

@pytest.fixture
def mock_user():
    # Mock user data for login and signup
    return {
        "username": "testuser",
        "password": "password123"
    }

@pytest.fixture
def new_user():
    return {
        "username": "newuser",
        "password": "newpass"
    }

def test_home(client):
    """Test the home route, should redirect to login if not logged in"""
    response = client.get('/')
    assert response.status_code == 302  # Should redirect
    assert b"login" in response.data  # Ensure it redirects to login

def test_login(client, mock_user):
    """Test the login functionality"""
    # Simulate the user signing up
    client.post('/signup', data=mock_user)
    
    # Attempt to login
    response = client.post('/login', data=mock_user)
    assert response.status_code == 302  # Should redirect to predict page after login
    assert b"predict" in response.data  # Should be redirected to the predict page

def test_login_invalid_credentials(client, mock_user):
    """Test invalid login credentials"""
    # Try logging in with incorrect credentials
    mock_user_invalid = { "username": "wronguser", "password": "wrongpass" }
    response = client.post('/login', data=mock_user_invalid)
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data  # Should show invalid credentials message

def test_signup(client, mock_user, new_user):
    """Test signup functionality"""
    # response = client.post('/signup', data=new_user)
    # assert response.status_code == 302  # Should redirect to login page after successful signup
    
    # Try to sign up with an existing username
    response_existing_user = client.post('/signup', data=mock_user)
    assert response_existing_user.status_code == 200
    assert b"Username already exists" in response_existing_user.data  # Should show username already exists

def test_predict(client, mock_user):
    """Test the predict functionality when logged in"""
    # Log in first
    client.post('/signup', data=mock_user)
    client.post('/login', data=mock_user)

    # Now test the predict route with valid data
    response = client.post('/predict', data={
        'humidity': 75,
        'wind_speed': 10,
        'weather_condition': 0,  # Assuming 0 is for 'Clear'
        'hour': 14,
        'day': 3,
        'month': 5,
        'day_of_year': 125
    })

    # Check if the response status code is 200 (successful)
    assert response.status_code == 200
    assert b"prediction" in response.data  # Assuming the prediction is displayed in the response

def test_logout(client, mock_user):
    """Test the logout functionality"""
    # Log in first
    client.post('/signup', data=mock_user)
    client.post('/login', data=mock_user)

    # Now test the logout route
    response = client.get('/logout')
    assert response.status_code == 302  # Should redirect to login page
    assert b"login" in response.data  # Should redirect to login

