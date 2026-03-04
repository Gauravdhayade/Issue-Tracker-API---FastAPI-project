# 🚀 Issue Tracker API (FastAPI)

A **Jira-like Issue Tracking Backend System** built using **FastAPI, SQLAlchemy, and MySQL**.
This project demonstrates a **clean architecture backend application** with authentication, organization management, project management, issue tracking, comments, and activity timeline.

---

# 📌 Features

### 🔐 Authentication

* User Registration
* JWT Login Authentication
* Refresh Token support

### 🏢 Organization Management

* Create organization
* View user organizations
* Add members with roles

### 📁 Project Management

* Create projects inside organizations
* View organization projects

### 🐞 Issue Management

* Create issue
* Assign issue to users
* Set issue priority
* Update issue status

### 💬 Comments System

* Add comment to issue
* Edit comment
* List issue comments

### 🕒 Activity Timeline

Track complete issue history:

* Status changes
* Comments activity

### 🔎 Issue Search

Filter issues by:

* Project
* Status
* Priority
* Assignee
* Keyword search

### 📄 Pagination

Efficient issue listing using:

GET /issues/project/{project_id}?page=1&limit=10

### ⚡ Async Notifications

Background notifications when:

* Issue assigned
* Issue status updated

---

# 🧱 Architecture (Clean Architecture)

```
API Layer (Routes)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Database Access)
        ↓
Models (SQLAlchemy ORM)
        ↓
Database (MySQL)
```

Project Structure:

```
fastapi-task/
│
├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   ├── core/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

# 🛠 Tech Stack

Backend Framework

* FastAPI

Database

* MySQL

ORM

* SQLAlchemy

Authentication

* JWT (python-jose)

Password Hashing

* Passlib (bcrypt)

Async Server

* Uvicorn

---

# ⚙️ Installation

Clone repository

```
git clone https://github.com/Gauravdhayade/Issue-Tracker-API---FastAPI-project.git
```

Move into project folder

```
cd fastapi-task
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows:

```
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run server

```
uvicorn app.main:app --reload
```

---

# 📚 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📊 API Modules

Authentication

```
POST /auth/register
POST /auth/login
POST /auth/refresh
```

Organizations

```
POST /organizations/
GET /organizations/my
POST /organizations/{org_id}/members
```

Projects

```
POST /projects/{org_id}
GET /projects/{org_id}
```

Issues

```
POST /issues/{project_id}
GET /issues/project/{project_id}
PUT /issues/{issue_id}/status
GET /issues/{issue_id}/timeline
GET /issues/search
```

Comments

```
POST /comments/{issue_id}
GET /comments/{issue_id}
PUT /comments/{comment_id}
```

---

# 📈 Example Workflow

1️⃣ Register user
2️⃣ Login to get JWT token
3️⃣ Create organization
4️⃣ Create project inside organization
5️⃣ Create issue in project
6️⃣ Assign issue to user
7️⃣ Add comments
8️⃣ Track activity in timeline

---

# 🎯 Future Improvements

* Email Notifications
* File Attachments
* Tagging System
* WebSocket real-time updates
* Frontend (React / Next.js)

---

# 👨‍💻 Author

**Gaurav Dhayade**

GitHub
https://github.com/Gauravdhayade
