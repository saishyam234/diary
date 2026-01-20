from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, cursor
from auth import token_required
import jwt, datetime, os

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "secret123")

# 🔐 Signup
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    password = generate_password_hash(data["password"])

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (data["username"], password)
    )
    db.commit()
    return jsonify({"message": "User created"}), 201


# 🔑 Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (data["username"],)
    )
    user = cursor.fetchone()

    # ✅ Check password
    if user and check_password_hash(user["password"], data["password"]):

        # 🔐 CREATE JWT TOKEN (ADD THIS HERE)
        token = jwt.encode(
            {
                "user_id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401



# 📘 CREATE Entry
@app.route("/api/diary", methods=["POST"])
@token_required
def add_entry(user_id):
    data = request.json

    cursor.execute(
        "INSERT INTO diary (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, data["title"], data["content"])
    )
    db.commit()
    return jsonify({"message": "Entry added"}), 201


# 📄 READ (Search + Date Filter + Pagination)
@app.route("/api/diary", methods=["GET"])
@token_required
def get_entries(user_id):
    search = request.args.get("search", "")
    start = request.args.get("start")
    end = request.args.get("end")
    page = int(request.args.get("page", 1))
    limit = 5
    offset = (page - 1) * limit

    sql = "SELECT * FROM diary WHERE user_id=%s"
    params = [user_id]

    if search:
        sql += " AND (title LIKE %s OR content LIKE %s)"
        params += [f"%{search}%", f"%{search}%"]

    if start and end:
        sql += " AND DATE(created_at) BETWEEN %s AND %s"
        params += [start, end]

    sql += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params += [limit, offset]

    cursor.execute(sql, params)
    return jsonify(cursor.fetchall())


# ✏️ UPDATE Entry
@app.route("/api/diary/<int:id>", methods=["PUT"])
@token_required
def update_entry(user_id, id):
    data = request.json

    cursor.execute(
        "UPDATE diary SET title=%s, content=%s WHERE id=%s AND user_id=%s",
        (data["title"], data["content"], id, user_id)
    )
    db.commit()
    return jsonify({"message": "Entry updated"})


# 🗑 DELETE Entry
@app.route("/api/diary/<int:id>", methods=["DELETE"])
@token_required
def delete_entry(user_id, id):
    cursor.execute(
        "DELETE FROM diary WHERE id=%s AND user_id=%s",
        (id, user_id)
    )
    db.commit()
    return jsonify({"message": "Entry deleted"})


if __name__ == "__main__":
    app.run(debug=True)
