#!/usr/bin/env python3
"""
DB module for ORM.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class for Object Relational Mapping"""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The User object added to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The User object found in the database.

        Raises:
            InvalidRequestError: If no keyword arguments are provided or
                                 if any of the arguments do not match the
                                 column names.
            NoResultFound: If no user is found.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided.")

        for key in kwargs.keys():
            if key not in User.__table__.columns:
                raise InvalidRequestError(f"Invalid column: {key}")

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found with the given criteria.")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The attributes to update.

        Raises:
            ValueError: If any of the arguments do not match the column names.
        """
        user = self.find_user_by(id=user_id)

        for key in kwargs.keys():
            if key not in User.__table__.columns:
                raise ValueError(f"Invalid column: {key}")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
