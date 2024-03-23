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
