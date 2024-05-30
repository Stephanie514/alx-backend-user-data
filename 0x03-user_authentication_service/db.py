#!/usr/bin/env python3
"""Database module for ORM operations using SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """Database class for ORM operations."""

    def __init__(self) -> None:
        """Initialize a new database instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Create and cache the session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **filters) -> User:
        """
        Find a user in the database by arbitrary keyword arguments.

        Args:
            **filters: Arbitrary keyword arguments to filter users.

        Returns:
            User: The first User object that matches the filter criteria.

        Raises:
            InvalidRequestError: If no arguments are provided or invalid column
                                 names are used.
            NoResultFound: If no user matches the filter criteria.
        """
        if not filters:
            raise InvalidRequestError(
                "No arguments provided to filter the user."
            )

        valid_columns = User.__table__.c.keys()

        for key in filters.keys():
            if key not in valid_columns:
                raise InvalidRequestError(f"Invalid column name: {key}")

        user = self._session.query(User).filter_by(**filters).first()
        if user is None:
            raise NoResultFound("No user found matching the criteria.")
        return user

    def update_user(self, user_id: int, **updates) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **updates: The attributes to update and their new values.

        Raises:
            ValueError: If an attribute does not correspond to a valid
                        user attribute.
        """
        user = self.find_user_by(id=user_id)
        valid_columns = User.__table__.c.keys()

        for key, value in updates.items():
            if key not in valid_columns:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
