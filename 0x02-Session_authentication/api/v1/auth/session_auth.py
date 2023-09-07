#!/usr/bin/env python3
"""Session auth implementation
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """Basic Authorization class
        authorization header getter
        authorization header decoder
    """
