#!/usr/bin/env python3
"""Encrypt password module
Author: Emmanuel
Date: 31 Aug 2023
"""
import bcrypt
# kept for changing salt if needed
salt = bcrypt.gensalt()


def hash_password(password: str) -> bytes:
    """generate a password hash with bcrypt
    """
    salt = "$2b$12$AfwGRkzsoLTw4fOXaKa8C.".encode('utf-8')
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if a hashed-password is valid or equal to hash generated
    """
    newHash: bytes = hash_password(password)
    return newHash == hashed_password
