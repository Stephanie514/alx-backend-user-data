#!/usr/bin/env python3
""" Flask app for user authentication """

from flask import Flask, jsonify, abort
from Flask import request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    """ Root path """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def create_user():
    """ Create a new user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        response_payload = {"email": email, "message": "user created"}
        return jsonify(response_payload)
    except ValueError:
        response_payload = {"message": "email already registered"}
        return jsonify(response_payload), 400


@app.route('/sessions', methods=['POST'])
def log_in():
    """ Logs in a user and returns session ID """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response_payload = {"email": email, "message": "logged in"}
    response = jsonify(response_payload)
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
