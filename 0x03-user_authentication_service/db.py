#!/usr/bin/env python3
"""
Database module for ORM with SQLAlchemy.
This module provides a Database class to interact with the users table.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class Database:
    """Database class for ORM operations on the users table."""

    def __init__(self) -> None:
        """Initialize the database engine and session."""
        self._db_engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._db_engine)
        Base.metadata.create_all(self._db_engine)
        self._db_session = None

    @property
    def session(self):
        """Create and cache the session object."""
        if self._db_session is None:
            SessionFactory = sessionmaker(bind=self._db_engine)
            self._db_session = SessionFactory()
        return self._db_session

    def add_user(self, user_email: str, user_hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            user_email (str): The user's email address.
            user_hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=user_email, hashed_password=user_hashed_password)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def find_user_by(self, **search_criteria) -> User:
        """
        Find a user in the database by arbitrary keyword arguments.

        Args:
            **search_criteria: Arbitrary keyword arguments to filter users.

        Returns:
            User: The first User object that matches the filter criteria.

        Raises:
            InvalidRequestError: If no arguments are provided or invalid
                                 column names are used.
            NoResultFound: If no user matches the filter criteria.
        """
        if not search_criteria:
            raise InvalidRequestError("No args provided to filter the user.")

        valid_columns = User.__table__.c.keys()

        for key in search_criteria.keys():
            if key not in valid_columns:
                raise InvalidRequestError(f"Invalid column name: {key}")

        user = self.session.query(User).filter_by(**search_criteria).first()
        if user is None:
            raise NoResultFound("No user found matching the criteria.")
        return user

    def update_user(self, user_id: int, **update_data) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **update_data: The attributes to update and their new values.

        Raises:
            ValueError: If an attribute does not correspond to a
                        valid user attribute.
        """
        user_to_update = self.find_user_by(id=user_id)
        valid_columns = User.__table__.c.keys()

        for key, value in update_data.items():
            if key not in valid_columns:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user_to_update, key, value)

        self.session.commit()
