#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, redirect, Response, jsonify, abort, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def basic() -> Response:
    """
    return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    email = request.form["email"]
    password = request.form["password"]
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    out = jsonify({"email": email, "message": "logged in"})
    out.set_cookie("session_id", session_id)
    return out


@app.route("/sessions", methods=['DELETE'])
def logout():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile")
def profile():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    email = request.form["email"]
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password() -> Response:
    """
    Update the password. If the token is invalid, catch the exception
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
