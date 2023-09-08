#!/usr/bin/env python3
""" Module of session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from flask import session
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_authenticator() -> str:
    """ POST /api/v1/session_auth/login
    Return:
      - JSON formated resu;ts
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if user is None:
        return None
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not (user.is_valid_password(password)):
        return jsonify({"error": "wrong password"}), 401
    auth_type = getenv("AUTH_TYPE", None)
    if auth_type is None:
        return None
    if auth_type == "session_auth":
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        out = jsonify(user.to_json())
        out.set_cookie("_my_session_id", session_id)
        return out
