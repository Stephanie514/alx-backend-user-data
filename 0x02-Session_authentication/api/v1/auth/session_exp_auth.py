#!/usr/bin/env python3
""" Module session in database
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session expiration class."""
    def __init__(self):
        """Initializing the SessionExpAuth class."""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """session with an expiration."""
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user_id associated with
        the session_id if not expired.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        current_time = datetime.now()
        session_expiry_time = created_at + timedelta(
            seconds=self.session_duration
        )

        if current_time > session_expiry_time:
            return None

        return session_dict.get('user_id')
