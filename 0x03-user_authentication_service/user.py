#!/usr/bin/env python3
"""
Define an SQLAlchemy model for the User table
Model attributes:
id: an integer primary key, auto-generated
email: a string representing the user's email
hashed_password: a string containing the hashed password
session_id: a string for session identification (optional)
reset_token: a string for password reset token (optional)
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ User model definition
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, email: str, hashed_password: str) -> None:
        """ Initialize a new User instance
        """
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self) -> str:
        """ Return a string representation of the User instance
        """
        return f"<User {self.email}>"

    def __str__(self) -> str:
        """ Return a readable string representation of the User
        """
        return f"<User {self.email}>"

    def __eq__(self, other: object) -> bool:
        """ Check if another User is equal to this User
        """
        if not isinstance(other, User):
            return False
        return self.email == other.email

    def __ne__(self, other: object) -> bool:
        """ Check if another User is not equal to this User
        """
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        """ Check if this User's email is less than another
            User's email
        """
        if not isinstance(other, User):
            return False
        return self.email < other.email

    def __gt__(self, other: object) -> bool:
        """ Check if this User's email is greater than another
            User's email
        """
        if not isinstance(other, User):
            return False
        return self.email > other.email

    def __hash__(self) -> int:
        """ Return the hash value of the User instance
        """
        return hash(self.email)

    def display_name(self) -> str:
        """ Generate a display name for the User
        """
        if (self.email is None and
                self.first_name is None and
                self.last_name is None):
            return ""
        if self.first_name is None and self.last_name is None:
            return f"{self.email}"
        if self.last_name is None:
            return f"{self.first_name}"
        if self.first_name is None:
            return f"{self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate the provided password against the stored
            hashed password
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.hashed_password, pwd)
