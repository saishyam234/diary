import jwt
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret123")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(data["user_id"], *args, **kwargs)
    return decorated


# {
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE3Njg5MDE5NDV9.vNJ0wPtXVsAbSKrDknQLVk_qUd0LNiA_247gf1rOrHU"
# }