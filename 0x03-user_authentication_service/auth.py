#!/usr/bin/env python3
"""
Hashing module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes
    """
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte, salt)
    return hashed
