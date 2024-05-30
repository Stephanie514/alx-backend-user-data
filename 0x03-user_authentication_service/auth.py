#!/usr/bin/env python3
"""Authentication management module"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the hashed bytes."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates and returns a unique UUID."""
    return str(uuid4())


class Auth:
    """Service class to manage authentication-related operations."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            decoded_password = hashed_password.decode('utf-8')
            new_user = self._db.add_user(email, decoded_password)
            return new_user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the user's login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for the user with the given email.

        Args:
            email (str): The user's email address.

        Returns:
            str: The new session ID, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves a user by their session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user associated with the session ID,
                  or None if not found.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Ends the session for the user with the given user ID.

        Args:
            user_id (int): The user's ID.
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user with the
        given email.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset password token.

        Raises:
           ValueError: If the user with the given email is not found.

        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User's email {} doesn't exist.".format(email))

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the user's password using the reset token.

        Args:
             reset_token (str): The reset token.
             password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid or user is not found.
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token.")

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
