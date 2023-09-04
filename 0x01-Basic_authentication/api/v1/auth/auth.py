#!/usr/bin/env python3
"""Authentication classs
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    """
    def __init__(self):
        """Initialization method
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A authorization handler
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header reader
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return a current user.
        """
        return None
