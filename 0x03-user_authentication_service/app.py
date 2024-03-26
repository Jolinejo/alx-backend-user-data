#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, Response, jsonify, abort, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
