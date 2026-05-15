<div align="center">

# ✅ Todo App

**The cleanest way to start your FastAPI journey**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Beginner Friendly](https://img.shields.io/badge/Level-Beginner-brightgreen?style=flat-square)]()

[← Back to Series](../README.md)

</div>

---

## 📌 About

The Todo App is the perfect entry point for this series. It's small enough to fully understand in one sitting, yet complete enough to teach all the patterns you'll use in larger projects. If you're new to FastAPI, start here.

## ✨ Features

- ✅ Create, read, update, and delete tasks
- 🔄 Mark tasks complete / incomplete
- 📅 Due date support
- 👤 User ownership of tasks
- 🔐 Simple authentication

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Auth | OAuth2 (basic) |

## 🚀 Getting Started

```bash
cd Todo
uv sync
uv run uvicorn main:app --reload
```

That's it — no database setup needed. SQLite creates itself automatically. Open **http://localhost:8000/docs** and start adding todos! 🎉

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a user |
| `POST` | `/auth/token` | Login |
| `GET` | `/todos` | List all your todos |
| `POST` | `/todos` | Create a todo |
| `GET` | `/todos/{id}` | Get a specific todo |
| `PUT` | `/todos/{id}` | Update a todo |
| `PUT` | `/todos/{id}/complete` | Toggle complete |
| `DELETE` | `/todos/{id}` | Delete a todo |

## 💡 Key Concepts Covered

- FastAPI app setup and project structure
- SQLAlchemy models and SQLite setup
- Pydantic schemas for request/response
- Dependency injection (`Depends`)
- Basic OAuth2 password flow
- CRUD operations end-to-end

## 📂 Project Structure

```
Todo/
├── main.py          # App entry point
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── database.py      # DB connection setup
├── routers/
│   ├── auth.py      # Auth routes
│   └── todos.py     # Todo routes
├── pyproject.toml
└── README.md
```

> 💡 **Tip:** After building this, head to [Project 1](../project1/README.md) to see the same concepts with a deeper dive, or jump to the [Blog API](../blog/README.md) to add a real database.
