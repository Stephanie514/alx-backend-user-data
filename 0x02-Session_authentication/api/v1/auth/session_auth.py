#!/usr/bin/env python3
"""
SessionAuth module
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    manages session authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): user ID for which to create a session.

        Returns:
            str: Session ID if creation is successful, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
