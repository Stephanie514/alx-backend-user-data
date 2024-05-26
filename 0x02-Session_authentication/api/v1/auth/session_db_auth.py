#!/usr/bin/env python3
""" Module Session in Database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Create a session ID and store it in the database"""
        if user_id is None:
            return None

        session_id = str(uuid.uuid4())
        session_duration = int(getenv('SESSION_DURATION', 0))
        expiration_time = (
            datetime.utcnow() + timedelta(seconds=session_duration)
        ).isoformat()

        new_session = UserSession(
            user_id=user_id,
            session_id=session_id,
            expiration_time=expiration_time
        )
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the user ID by session ID"""
        if session_id is None:
            return None

        user_session = UserSession.find_by(session_id=session_id)
        if user_session is None or self.is_session_expired(user_session):
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the user session based on session ID from
           the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.destroy_by(session_id=session_id)
        return True
