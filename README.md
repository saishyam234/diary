# 📔 Personal Diary App (Full-Stack)

A **production-ready Personal Diary application** built with **Flask + MySQL**, featuring **JWT authentication**, **refresh tokens**, **role-based access control**, and a **Bootstrap UI**.

This project demonstrates **real-world backend authentication patterns** and a simple frontend to interact with secured APIs.

---

## 🚀 Features

### 🔐 Authentication & Security

* User **Signup & Login**
* Password hashing using **Werkzeug**
* **JWT Access Tokens** (short-lived)
* **Refresh Tokens** (long-lived)
* Automatic **token expiry handling**
* **Logout** support (token removal)
* **Role-Based Access Control (RBAC)** (`user`, `admin`)

### 📘 Diary Management

* Create diary entries
* Read diary entries (user-specific)
* Server-side validation
* Secure access using JWT middleware

### 🎨 User Interface

* Clean **Bootstrap 5** UI
* Frontend written in **HTML + JavaScript**
* Token storage using **localStorage**
* Automatic refresh token handling

### 🛠 Developer Friendly

* RESTful API design
* Modular Flask structure
* Easy to deploy (Render / Railway)
* GitHub-ready project

---

## 🧱 Tech Stack

| Layer      | Technology                  |
| ---------- | --------------------------- |
| Backend    | Python, Flask               |
| Database   | MySQL                       |
| Auth       | JWT (PyJWT)                 |
| Security   | Werkzeug password hashing   |
| Frontend   | HTML, Bootstrap, JavaScript |
| Deployment | Render / Railway            |

---

## 📁 Project Structure

```
diary-api/
│
├── app.py
├── auth.py
├── db.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── app.js
│
└── .gitignore
```

---

## 🔐 API Endpoints

### Authentication

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| POST   | `/api/signup`  | Register a new user      |
| POST   | `/api/login`   | Login and receive tokens |
| POST   | `/api/refresh` | Refresh access token     |

### Diary

| Method | Endpoint     | Description        |
| ------ | ------------ | ------------------ |
| POST   | `/api/diary` | Add diary entry    |
| GET    | `/api/diary` | Read diary entries |

### Admin (RBAC)

| Method | Endpoint           | Role       |
| ------ | ------------------ | ---------- |
| GET    | `/api/admin/users` | Admin only |

---

## 🗄 Database Setup

```sql
CREATE DATABASE diary_db;
USE diary_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE diary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## ▶ Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set environment variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=diary_db
SECRET_KEY=supersecretkey
```

### 3️⃣ Run the app

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🔐 Authentication Flow

1. User logs in → receives **access token + refresh token**
2. Access token is used for API calls
3. If access token expires → refresh token generates a new one
4. Logout clears tokens from browser

---

## 🧪 Validation & Error Handling

* Empty input validation (frontend + backend)
* Expired token detection
* Unauthorized access handling
* Role-based access denial

---

## 🌍 Deployment

This app can be deployed on:

* **Render**
* **Railway**

Start command:

```
gunicorn app:app
```

Add environment variables in the platform dashboard.

---

## 📌 Future Improvements

* React frontend
* HTTP-only cookies
* Edit/Delete diary entries
* Search & pagination
* Swagger / OpenAPI docs
* Unit testing

---

## 👨‍💻 Author

**Saishyam Sajane**
GitHub: [https://github.com/saishyam234](https://github.com/saishyam234)

---

⭐ If you like this project, give it a star on GitHub!

