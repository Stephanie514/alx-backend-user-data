#!/usr/bin/env python3
"""
User model definition using SQLAlchemy.
This module defines the User model for the users table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of user.
        hashed_password (str): The password of the user.
        session_id (str, optional): The session ID for the user.
        reset_token (str, optional): Reset token for password recovery.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
