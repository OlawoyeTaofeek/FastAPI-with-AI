<div align="center">

# 📸 Instagram Clone

**A social media backend with image uploads, follows & feeds**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![WebSockets](https://img.shields.io/badge/WebSockets-enabled-brightgreen?style=flat-square)](https://fastapi.tiangolo.com/advanced/websockets/)

[← Back to Series](../README.md)

</div>

---

## 📌 About

The Instagram Clone project is one of the most feature-rich in this series. It dives deep into file handling, social graph relationships, real-time notifications, and feed generation — skills directly applicable to any social platform.

## ✨ Features

- 📷 Image upload (local or cloud)
- 👥 Follow / Unfollow users
- 🖼️ Personalized photo feed
- ❤️ Likes and comments
- 🔔 Real-time notifications (WebSockets)
- 🔍 User search and discovery

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| File Storage | Cloudinary / AWS S3 |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Real-time | WebSockets |
| Auth | JWT |

## 🚀 Getting Started

```bash
cd instagramClone
uv sync
# Add cloud storage credentials to .env
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/posts` | Upload a photo post |
| `GET` | `/feed` | Get personalized feed |
| `POST` | `/users/{id}/follow` | Follow a user |
| `DELETE` | `/users/{id}/follow` | Unfollow a user |
| `POST` | `/posts/{id}/like` | Like a post |
| `POST` | `/posts/{id}/comments` | Comment on a post |
| `GET` | `/users/search` | Search users |
| `WS` | `/ws/notifications` | Real-time notifications |

## 💡 Key Concepts Covered

- Multipart file uploads in FastAPI
- Self-referential relationships (User follows User)
- Feed ranking and pagination with `OFFSET`/`LIMIT`
- Cloud storage integration (Cloudinary/S3)
- WebSocket connections for real-time features
- Social graph queries with SQLAlchemy
