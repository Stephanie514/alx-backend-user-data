#!/usr/bin/env python3
"""
SessionAuth module
"""
from flask import Blueprint, request, jsonify
from api.v1.auth.auth import Auth
import uuid
from models.user import User
import os
from .auth import Auth
import uuid


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

    def session_cookie(self, request=None):
        """Returns the cookie from a request"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)

    def destroy_session(self, request=None):
        """Destroys a user session / logout"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if session_id not in self.user_id_by_session_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
