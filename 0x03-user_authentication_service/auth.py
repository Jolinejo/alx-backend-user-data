#!/usr/bin/env python3
"""
Hashing module
"""

from typing import Union
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _generate_uuid() -> str:
    """
     returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        save the user to the database using self._db and return the User
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        expect email and password required arguments and return a boolean
        """
        byte = password.encode('utf-8')
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(byte, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        takes an email string argument and returns the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        It takes a single session_id string argument
        and returns the corresponding User or None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        The method updates the corresponding user’s session ID to None
        """
        self._db.update_user(user_id=user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate a UUID and update the user’s reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update the user’s hashed_password field
        with the new hashed password
        """
        if reset_token is None:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user_id=user.id,
                                 hashed_password=hashed,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes
    """
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte, salt)
    return hashed
