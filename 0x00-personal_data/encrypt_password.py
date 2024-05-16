#!/usr/bin/env python3

"""
encrypt_password module

This module provides functions for hashing and validating passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    This validates a plain-text password against a hashed
    password using bcrypt.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the plain-text password to
        be validated.

    Returns:
        bool: True if the plain-text password matches the hashed
        password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


if __name__ == "__main__":
    # Testing the hash_password function
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password)

    # Testing the is_valid function
    print(is_valid(hashed_password, password))
