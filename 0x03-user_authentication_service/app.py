#!/usr/bin/env python3
""" Flask application module
"""
from flask import Flask, jsonify, abort
from flask import request
from auth import Auth

# Initializing the Flask application
app = Flask(__name__)
# Creating an instance of the Auth class
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """ Handle requests to the root URL.
        Returns a JSON response with a welcome message.
    """
    response_payload = {
        "message": "Bienvenue"
    }
    return jsonify(response_payload)


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Register a new user.
        Expects form data with 'email' and 'password' fields.
        Returns a JSON response indicating success or failure.
    """
    email = request.form.get('email')  # Getting the email from the form data
    password = request.form.get('password')
    try:
        # Attempting to register the user
        user = AUTH.register_user(email, password)
        response_payload = {
            "email": email,
            "message": "user created"
        }
        return jsonify(response_payload)
    except Exception:
        # If registration fails (user already exists), return an error message
        response_payload = {
            "message": "email already registered"
        }
        return jsonify(response_payload), 400


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """ Log in an existing user.
        Expects form data with 'email' and 'password' fields.
        Returns a JSON response with the session ID if successful.
    """
    try:
        email = request.form['email']  # Getting the email from the form data
        password = request.form['password']
    except KeyError:
        # If email or password is not provided, return a 400 error
        abort(400)

    if not AUTH.valid_login(email, password):
        # If login credentials are invalid, return a 401 error
        abort(401)

    # Creating a session for the user and get the session ID
    session_id = AUTH.create_session(email)

    # Preparing the success message
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    # Setting the session ID as a cookie in the response
    response.set_cookie("session_id", session_id)

    return response


# Running the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
