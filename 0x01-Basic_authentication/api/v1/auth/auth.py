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
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if str(path) + "/" in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header reader
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """return a current user.
        """
        return None
