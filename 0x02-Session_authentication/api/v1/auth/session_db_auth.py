#!/usr/bin/env python3
""" Module Session in Database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv

class SessionDBAuth(SessionExpAuth):
    def __init__(self):
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None
        user_session = UserSession.get(session_id)
        if user_session is None:
            return None
        user_id = user_session.user_id
        if self.session_duration <= 0:
            return user_id
        # check session expiration
        return user_id

    def destroy_session(self, request=None):
        # Adding logic to destroy session
        pass
