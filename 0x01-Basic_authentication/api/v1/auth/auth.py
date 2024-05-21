#!/usr/bin/env python3
""" This is the Authentication module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checking if authentication is required for a given path"""
        if path is None:
            return True
        if not excluded_paths:
            return True

        # path ends with a slash
        if path[-1] != '/':
            path += '/'

        for ep in excluded_paths:
            # each excluded path ends with a slash
            if ep[-1] != '/':
                ep += '/'
            if path == ep:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns None as placeholder"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None as placeholder"""
        return None
