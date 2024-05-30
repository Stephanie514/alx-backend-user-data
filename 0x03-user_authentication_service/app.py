#!/usr/bin/env python3
""" Flask application module
"""
from flask import Flask, jsonify, abort  # Import necessary Flask modules
from flask import request  # Import request module from Flask
from auth import Auth  # Import the Auth class from the auth module

# Initializing the Flask application
app = Flask(__name__)
# instance of the Auth class
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
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        response_payload = {
            "email": email,
            "message": "user created"
        }
        return jsonify(response_payload)
    except Exception:
        # If user already exists, return an error message
        response_payload = {
            "message": "email already registered"
        }
        return jsonify(response_payload), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def log_in():
    """ Log in an existing user.
        Expects form data with 'email' and 'password' fields.
        Returns a JSON response with the session ID if successful.
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        # If email or password is not provided, return a 400 error
        abort(400)

    if not AUTH.valid_login(email, password):
        # If the login credentials are invalid, return a 401 error
        abort(401)

    # Create a session for the user and get the session ID
    session_id = AUTH.create_session(email)

    # Prepare the success message
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    # Set the session ID as a cookie in the response
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def log_out():
    """ Log out the current user.
        Expects the session ID as a cookie.
        Returns a redirect to the root URL if successful.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        # If no session ID is found in the cookies, return a 403 error
        abort(403)

    if not AUTH.destroy_session(session_id):
        # If the session could not be destroyed, return a 403 error
        abort(403)

    # Redirect to the root URL after successful logout
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Get the profile of the logged-in user.
        Expects the session ID as a cookie.
        Returns a JSON response with the user's email if successful.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        # If no session ID is found in the cookies, return a 403 error
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        # If no user is found for the session ID, return a 403 error
        abort(403)

    # Return the user's email in the response payload
    response_payload = {"email": user.email}
    return jsonify(response_payload)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Generate a password reset token for a user.
        Expects form data with the 'email' field.
        Returns a JSON response with the reset token if successful.
    """
    email = request.form.get('email')
    if email is None:
        # If no provided email, return a 400 error
        abort(400)

    try:
        # Generating a reset token for the user
        reset_token = AUTH.get_reset_password_token(email)
        response_payload = {"email": email, "reset_token": reset_token}
        return jsonify(response_payload)
    except Exception:
        # If email is not registered, return a 403 error
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update the user's password.
        Expects form data with 'email', 'reset_token', and
        'new_password' fields.
        Returns a JSON response indicating success or failure.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not all([email, reset_token, new_password]):
        # If any required fields are missing, return a 400 error
        abort(400)

    try:
        # Attempt to update the user's password
        AUTH.update_password(reset_token, new_password)
        response_payload = {"email": email, "message": "Password updated"}
        return jsonify(response_payload)
    except Exception:
        # If the reset token is invalid or the update fails, return a 403 error
        abort(403)


# Running the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
