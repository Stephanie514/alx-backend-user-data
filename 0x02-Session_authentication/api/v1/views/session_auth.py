#!/usr/bin/env python3
"""
SessionAuth module
"""
from flask import Blueprint, request, jsonify
import uuid
from models.user import User
import os
from api.v1.auth.session_auth import SessionAuth

session_auth = Blueprint('session_auth', __name__)


@session_auth.route(
    '/auth_session/login',
    methods=['POST'],
    strict_slashes=False
)
def login():
    """Handles user login for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth  # avoid circular import

    session_id = auth.create_session(user.id)
    user_dict = user.to_json()
    response = jsonify(user_dict)
    session_name = os.getenv("SESSION_NAME")

    response.set_cookie(session_name, session_id)
    return response
