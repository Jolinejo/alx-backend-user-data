#!/usr/bin/env python3
""" Session class
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64
from models.user import User


class SessionAuth(Auth):
    """
    validate if everything inherits correctly without any overloading
    validate the “switch” by using environment variables
    """
    pass
