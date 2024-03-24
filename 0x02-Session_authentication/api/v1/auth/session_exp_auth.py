#!/usr/bin/env python3
""" exp class
"""
from flask import request
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    expiration date class
    """
    def __init__(self):
        """
        init func
        """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        session creation
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        super overload
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        tot = created_at + timedelta(seconds=self.session_duration)
        if tot < datetime.now():
            return None
        return self.user_id_by_session_id[session_id]['user_id']
