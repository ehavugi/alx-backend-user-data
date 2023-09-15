#!/usr/bin/env python3
"""Auth  module
    _hash_password -> return hash
"""
import bcrypt
salt = bcrypt.gensalt()


def _hash_password(password):
    """return a password hash
    """
    bytes = password.encode("utf-8")
    return bcrypt.hashpw(bytes, salt)
