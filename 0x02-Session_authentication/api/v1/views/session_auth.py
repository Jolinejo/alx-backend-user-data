#!/usr/bin/env python3
""" Module of session views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    handles all routes for the Session authentication.
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    if not pwd or pwd is None:
        return jsonify({"error": "password missing"}), 400
    attr = {'email': email}
    listi = User.search(attr)
    if not listi:
        return jsonify({"error": "no user found for this email"}), 404
    if listi[0].is_valid_password(pwd) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(listi[0].id)
    out = jsonify(listi[0].to_json())
    cookie_name = os.getenv('SESSION_NAME')
    out.set_cookie(cookie_name, session_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    for deleting the Session ID
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
