#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, Response, jsonify, abort, request


app = Flask(__name__)


@app.route("/")
def basic() -> Response:
    """
    return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
