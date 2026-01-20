# 📔 Personal Diary App (REST API)

A secure Personal Diary application built with Flask and MySQL, featuring JWT authentication, CRUD operations, search, filtering, pagination, and cloud deployment support.

## 🚀 Features
- JWT-based authentication (Signup/Login)
- Password hashing with Werkzeug
- RESTful API architecture
- CRUD diary entries
- Search & date-based filtering
- Pagination support
- MySQL database integration
- Cloud deployable (Render/Railway)

## 🛠 Tech Stack
- Backend: Python, Flask
- Database: MySQL
- Security: JWT, Password Hashing
- Deployment: Render / Railway

## 🔐 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /api/signup | Register user |
| POST | /api/login | Login user |
| POST | /api/diary | Add entry |
| GET | /api/diary | List entries |
| PUT | /api/diary/:id | Update entry |
| DELETE | /api/diary/:id | Delete entry |

## ▶ Run Locally
```bash
pip install -r requirements.txt
python app.py
