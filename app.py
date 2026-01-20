from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, cursor
from auth import token_required, role_required
import jwt, datetime, os

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "secret123")

# ---------------- UI ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SIGNUP ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "All fields required"}), 400

    password = generate_password_hash(data["password"])

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (data["username"], password)
    )
    db.commit()
    return jsonify({"message": "User created"}), 201

# ---------------- LOGIN ----------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    cursor.execute("SELECT * FROM users WHERE username=%s", (data["username"],))
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], data["password"]):
        access_token = jwt.encode({
            "user_id": user["id"],
            "role": user.get("role", "user"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }, SECRET_KEY, algorithm="HS256")

        refresh_token = jwt.encode({
            "user_id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    return jsonify({"error": "Invalid credentials"}), 401

# ---------------- REFRESH TOKEN ----------------
@app.route("/api/refresh", methods=["POST"])
def refresh():
    data = request.json
    try:
        payload = jwt.decode(data["refresh_token"], SECRET_KEY, algorithms=["HS256"])
        new_access = jwt.encode({
            "user_id": payload["user_id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"access_token": new_access})
    except:
        return jsonify({"error": "Invalid refresh token"}), 401

# ---------------- ADD DIARY ----------------
@app.route("/api/diary", methods=["POST"])
@token_required
def add_entry(user_id):
    data = request.json

    if not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title & content required"}), 400

    cursor.execute(
        "INSERT INTO diary (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, data["title"], data["content"])
    )
    db.commit()
    return jsonify({"message": "Entry added"}), 201

# ---------------- READ DIARY ----------------
@app.route("/api/diary", methods=["GET"])
@token_required
def get_entries(user_id):
    cursor.execute("SELECT * FROM diary WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    return jsonify(cursor.fetchall())

# ---------------- ADMIN ROUTE ----------------
@app.route("/api/admin/users")
@token_required
@role_required("admin")
def admin_users(user_id):
    cursor.execute("SELECT id, username, role FROM users")
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
