#!/usr/bin/env python3
"""Basic auth implementation
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authorization class
        authorization header getter
        authorization header decoder
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Read authorization header and remove Basic Keyword
           and return the header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode a base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """return user credential given a decoded base64 auth
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if not (":" in decoded_base64_authorization_header):
            return None, None
        decoded = decoded_base64_authorization_header.split(":")
        return decoded[0], decoded[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """return a user object given user_email and user password
        """
        if user_email is None or not(isinstance(user_email, str)):
            return None
        if user_pwd is None or not(isinstance(user_pwd, str)):
            return None

        if User:
            newUser = User.search({"email": user_email})
            if len(newUser) <= 0:
                return None
            newUser = newUser[0]
            if isinstance(newUser, User):
                if newUser.is_valid_password(user_pwd):
                    return newUser
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return user Object from header in a request
        by decoding and finding the user
        """
        if request is None:
            return None
        auth_header_r = request.headers.get("Authorization", None)
        auth_header = self.extract_base64_authorization_header(auth_header_r)
        auth_decoded = self.decode_base64_authorization_header(auth_header)
        (user_email, user_pwd) = self.extract_user_credentials(auth_decoded)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user

    def extract_user_credentials(self, decoded_base64_authorization_header):
        """ return user credential given a decoded base64 auth.
        allow : in the password
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if not (":" in decoded_base64_authorization_header):
            return None, None
        decoded = decoded_base64_authorization_header.split(":")
        if len(decoded) == 2:
            return decoded[0], decoded[1]
        return decoded[0], ":".join(decoded[1:])
