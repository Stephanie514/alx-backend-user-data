#!/usr/bin/env python3
""" Flask app for user authentication """

from flask import Flask, jsonify, abort, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


# The Root path
@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """ Root path """
    response_payload = {"message": "Welcome"}
    return jsonify(response_payload)


# This Registers a new user
@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        response_payload = {"email": email, "message": "User created"}
        return jsonify(response_payload)
    except Exception:
        response_payload = {"message": "Email already registered"}
        return jsonify(response_payload), 400


# This logs in a user and returns session ID
@app.route('/sessions', methods=['POST'])
def log_in():
    """ Logs in a user and returns session ID """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response_payload = {"email": email, "message": "Logged in"}
    response = jsonify(response_payload)
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
