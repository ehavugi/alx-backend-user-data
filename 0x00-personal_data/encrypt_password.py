#!/usr/bin/env python3
"""Encrypt password module
Author: Emmanuel
Date: 31 Aug 2023
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """generate a password hash with bcrypt
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if a hashed-password is valid or equal to hash generated
    """
    newHash: bytes = hash_password(password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
