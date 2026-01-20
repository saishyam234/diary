import jwt
from functools import wraps
from flask import request, jsonify
from jwt import ExpiredSignatureError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret123")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(data["user_id"], *args, **kwargs)
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(user_id, *args, **kwargs):
            auth = request.headers.get("Authorization")
            token = auth.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if data.get("role") != role:
                return jsonify({"error": "Access denied"}), 403

            return f(user_id, *args, **kwargs)
        return wrapper
    return decorator
