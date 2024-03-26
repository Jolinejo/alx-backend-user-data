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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
