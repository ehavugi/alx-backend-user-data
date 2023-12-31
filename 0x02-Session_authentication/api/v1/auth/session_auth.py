#!/usr/bin/env python3
"""Session auth implementation
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Basic Authorization class
        authorization header getter
        authorization header decoder
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session given user_id
        """
        if user_id is None:
            return None
        if not(isinstance(user_id, str)):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get a user_id for a session given session_id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """get the current user
        """
        cookie_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_id)
        return User.get(user_id)
