#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authuntication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ not used yet
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ not used yet
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ not used yet
        """
        return None
