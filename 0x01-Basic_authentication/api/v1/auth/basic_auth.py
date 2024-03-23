#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """ C lass for basic Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication:
        """

        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header:
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        i = decoded_base64_authorization_header.find(':')
        name = decoded_base64_authorization_header[:i]
        password = decoded_base64_authorization_header[i+1:]
        return (name, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on
        his email and password."""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            attr = {'email': user_email}
            listi = User.search(attr)
        except Exception:
            return None
        for user in listi:
            if user.is_valid_password(user_pwd):
                return user
        return None
