<div align="center">

# 📝 Blog API

**A production-ready blog backend built with FastAPI**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)

[← Back to Series](../README.md)

</div>

---

## 📌 About

The Blog API project demonstrates how to build a full-featured content management backend. It covers authentication, relational data modeling, and clean API design — the backbone of any real-world web service.

## ✨ Features

- 🔐 JWT-based user authentication & registration
- ✍️ Full CRUD for blog posts
- 🏷️ Categories and tags
- 💬 Nested comments
- 📄 Pagination and filtering
- 👤 Author profiles

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL |
| Auth | JWT / OAuth2 |
| Validation | Pydantic v2 |

## 🚀 Getting Started

```bash
cd blog
uv sync
# Configure your .env file (see .env.example)
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Get access token |
| `GET` | `/posts` | List all posts |
| `POST` | `/posts` | Create a post |
| `GET` | `/posts/{id}` | Get a single post |
| `PUT` | `/posts/{id}` | Update a post |
| `DELETE` | `/posts/{id}` | Delete a post |
| `POST` | `/posts/{id}/comments` | Add a comment |

## 💡 Key Concepts Covered

- Setting up SQLAlchemy with async support
- Designing relational schemas (Users → Posts → Comments)
- Password hashing with `passlib`
- JWT token creation and verification
- Dependency injection for auth guards
- Alembic migration workflow

## 🌐 Interactive Docs

Once running, visit:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc
