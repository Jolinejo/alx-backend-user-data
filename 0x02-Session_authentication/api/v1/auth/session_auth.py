#!/usr/bin/env python3
""" Session class
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    validate if everything inherits correctly without any overloading
    validate the “switch” by using environment variables
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        """
        req_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(req_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        deletes the user session / logout:
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
