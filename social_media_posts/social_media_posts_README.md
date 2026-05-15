<div align="center">

# 📱 Social Media Posts API

**A Twitter/X-style post system with likes, comments & authentication**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)

[← Back to Series](../README.md)

</div>

---

## 📌 About

The Social Media Posts project steps up from the Blog API by adding social features: likes, user interactions, and an activity feed. It's an excellent bridge between foundational CRUD and the more complex Instagram Clone project.

## ✨ Features

- 📝 Create, edit, and delete posts
- ❤️ Like / unlike posts
- 💬 Threaded comments
- 👤 User profiles and auth
- 📰 Chronological activity feed
- 🔒 Owner-only post editing

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Auth | OAuth2 + JWT |
| Validation | Pydantic v2 |

## 🚀 Getting Started

```bash
cd social_media_posts
uv sync
# Configure DATABASE_URL in .env
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Create account |
| `POST` | `/auth/login` | Login and get token |
| `GET` | `/posts` | Get all posts (feed) |
| `POST` | `/posts` | Create a post |
| `GET` | `/posts/{id}` | View a post |
| `PUT` | `/posts/{id}` | Edit your post |
| `DELETE` | `/posts/{id}` | Delete your post |
| `POST` | `/posts/{id}/like` | Like a post |
| `POST` | `/posts/{id}/comments` | Comment on a post |
| `GET` | `/users/{id}/posts` | All posts by a user |

## 💡 Key Concepts Covered

- Ownership checks (only post authors can edit/delete)
- Toggle logic for likes (like → unlike)
- Foreign key relationships across Users, Posts, Likes, Comments
- Filtering and sorting feed results
- Response schema design to avoid over-fetching
