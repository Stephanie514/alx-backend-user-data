#!/usr/bin/env python3
""" This is the Authentication module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class that manages API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False as placeholder"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None as placeholder"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None as placeholder"""
        return None
