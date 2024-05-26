#!/usr/bin/env python3
"""Module for managing user sessions with file-based persistence."""

import json
import os
from models.base import Base


class UserSession(Base):
    """UserSession model for managing user sessions."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.expiry_time = kwargs.get('expiration_time')

    def save(self):
        """Save the current session to the file."""
        session_file = 'user_sessions.json'
        sessions = []

        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                sessions = json.load(f)

        sessions.append(self.to_dict())
        with open(session_file, 'w') as f:
            json.dump(sessions, f)

    @classmethod
    def find_by_session_id(cls, session_id):
        """Retrieve a session by session_id."""
        session_file = 'user_sessions.json'

        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                sessions = json.load(f)
                for session in sessions:
                    if session.get('session_id') == session_id:
                        return cls(**session)

        return None

    @classmethod
    def destroy_by_session_id(cls, session_id):
        """Remove a session by session_id."""
        session_file = 'user_sessions.json'

        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                sessions = json.load(f)

            filtered_sessions = [session for session in sessions
                                 if session.get('session_id') != session_id]
            sessions = filtered_sessions

            with open(session_file, 'w') as f:
                json.dump(sessions, f)

    def to_dict(self):
        """Convert the session instance to a dictionary."""
        return {
            'user_id': self.user_id,
            'session_id': self.session_id,
            'expiration_time': self.expiry_time
        }
