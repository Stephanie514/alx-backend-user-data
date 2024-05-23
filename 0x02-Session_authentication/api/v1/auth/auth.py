#!/usr/bin/env python3
"""
Auth module
"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """
    Auth class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This checks if a path requires authentication based on excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that are
                                        excluded from authentication.

        Returns:
            bool: True if authentication is required, False if not required.
        """
        if path is None:
            return True
        if not excluded_paths or not excluded_paths:
            return True

        for ep in excluded_paths:
            if ep.endswith('*'):
                if path.startswith(ep[:-1]):
                    return False
            elif path == ep or path.startswith(ep.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        This Retrieves the Authorization header from the request.

        Args:
            request: The request object.

        Returns:
            str: value of the Authorization header if present,
                 otherwise None.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Args:
            request: The request object.

        Returns:
            User: The current user if present, otherwise None.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.

        Args:
            request: The request object.

        Returns:
            str: The value of the cookie named SESSION_NAME if found in the
                 request cookies, otherwise None.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
