#!/usr/bin/env python3
"""
SessionAuth module
"""
from flask import Blueprint, request, jsonify
from api.v1.auth.auth import Auth
import uuid
from models.user import User
import os


class SessionAuth(Auth):
    """
    SessionAuth class for managing session authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The Session ID if creation is successful, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This returns User ID based on a Session ID.

        Args:
            session_id (str): Session ID for which to retrieve the user ID.

        Returns:
            str: User ID if session_id is found in user_id_by_session_id,
                 otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)


session_auth = Blueprint('session_auth', __name__)

@session_auth.route('/auth_session/login',
                   methods=['POST'], strict_slashes=False)
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

    session_id = SessionAuth().create_session(user.id)
    user_dict = user.to_json()
    response = jsonify(user_dict)
    session_name = os.getenv("SESSION_NAME")

    response.set_cookie(session_name, session_id)
    return response
