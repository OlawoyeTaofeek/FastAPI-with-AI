<div align="center">

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="200"/>

# ⚡ FastAPI Mastery Series

**A complete, project-driven journey from zero to production-ready FastAPI applications.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=for-the-badge)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> *Learn FastAPI by building real-world applications — from blog APIs to ML-powered services.*

</div>

---

## 📖 About This Series

This repository is a **hands-on FastAPI learning series** where each folder is a fully self-contained project. Rather than learning in isolation, you'll build actual applications that mirror real-world use cases — solidifying your understanding at every level.

Whether you're new to FastAPI or leveling up your backend skills, this series grows with you.

---

## 🗂️ Projects Overview

| # | Project | Description | Key Concepts |
|---|---------|-------------|--------------|
| 1 | [📝 Blog API](#-blog-api) | Full-featured blog backend | CRUD, Auth, Schemas |
| 2 | [🛒 E-Commerce API](#-e-commerce-api) | Product & order management | Relations, Pagination, Payments |
| 3 | [🤖 End-to-End ML with FastAPI](#-end-to-end-ml-with-fastapi) | Serve ML models via API | ML integration, Background tasks |
| 4 | [📸 Instagram Clone](#-instagram-clone) | Social media backend | File uploads, Feed, Follows |
| 5 | [💬 MyChatGPT](#-mychatgpt) | LLM-powered chat API | Streaming, OpenAI/Anthropic SDK |
| 6 | [🚀 Project 1](#-project-1) | Foundational starter project | Routing, Models, Validation |
| 7 | [📱 Social Media Posts](#-social-media-posts) | Posts & engagement API | Likes, Comments, Auth |
| 8 | [✅ Todo App](#-todo-app) | Classic task manager | Beginner-friendly, Full CRUD |

---

## 🏗️ Projects

### 📝 Blog API
> `./blog/`

A production-style blog backend covering everything you need for a real REST API.

**Features:** User auth with JWT · Post CRUD · Categories & Tags · Comments · Pagination  
**Stack:** FastAPI · SQLAlchemy · Alembic · PostgreSQL · Pydantic v2  
[→ View Project README](./blog/README.md)

---

### 🛒 E-Commerce API
> `./ecommerce/`

A scalable e-commerce backend handling products, carts, orders, and payments.

**Features:** Product catalog · Cart management · Order processing · Role-based access  
**Stack:** FastAPI · SQLAlchemy · Stripe integration · Redis (caching)  
[→ View Project README](./ecommerce/README.md)

---

### 🤖 End-to-End ML with FastAPI
> `./EndToEndMLWithFastAPI/`

Deploy a real machine learning model as a REST API — from training to serving.

**Features:** Model training pipeline · Prediction endpoints · Background jobs · Model versioning  
**Stack:** FastAPI · Scikit-learn / PyTorch · Celery · Docker  
[→ View Project README](./EndToEndMLWithFastAPI/README.md)

---

### 📸 Instagram Clone
> `./instagramClone/`

A social media backend with image uploads, follows, and a personalized feed.

**Features:** Image upload (S3/local) · Follow system · Feed algorithm · Stories  
**Stack:** FastAPI · SQLAlchemy · Cloudinary / AWS S3 · WebSockets  
[→ View Project README](./instagramClone/README.md)

---

### 💬 MyChatGPT
> `./MyChatGPT/`

Build your own ChatGPT-like application using FastAPI and LLM APIs.

**Features:** Streaming responses · Conversation history · Multiple model support · System prompts  
**Stack:** FastAPI · OpenAI / Anthropic SDK · SSE · SQLAlachemy, LangChain, LangGraph  
[→ View Project README](./MyChatGPT/README.md)

---

### 🚀 Project 1
> `./project1/`

The foundational project — your first real FastAPI app with all the essentials.

**Features:** Path & query params · Request body · Response models · Error handling  
**Stack:** FastAPI · Pydantic v2 · Uvicorn  
[→ View Project README](./project1/README.md)

---

### 📱 Social Media Posts
> `./social_media_posts/`

A Twitter/X-style post system with likes, comments, and user interactions.

**Features:** Create/edit posts · Like & comment · User profiles · Activity feed  
**Stack:** FastAPI · SQLAlchemy · PostgreSQL · OAuth2  
[→ View Project README](./social_media_posts/README.md)

---

### ✅ Todo App
> `./Todo/`

The perfect beginner project — clean, simple, and complete.

**Features:** Task CRUD · Status tracking · Due dates · User ownership  
**Stack:** FastAPI · SQLite · Pydantic v2  
[→ View Project README](./Todo/README.md)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FAST_API.git
cd FAST_API
```

### Setup with uv (Recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to any project
cd Todo

# Create virtual environment and install dependencies
uv sync

# Run the app
uv run uvicorn main:app --reload
```

### Setup with pip

```bash
cd Todo
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://localhost:8000/docs** to explore the interactive API docs. 🎉

---

## 📚 Learning Path

Follow this order if you're new to FastAPI:

```
project1  →  Todo  →  blog  →  social_media_posts
    ↓
ecommerce  →  instagramClone
    ↓
MyChatGPT  →  EndToEndMLWithFastAPI
```

Each project introduces new concepts that build on the previous one.

---

## 🛠️ Tech Stack Across the Series

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework |
| **Pydantic v2** | Data validation & serialization |
| **SQLAlchemy** | ORM & database management |
| **Alembic** | Database migrations |
| **uv** | Fast Python package manager |
| **Uvicorn** | ASGI server |
| **JWT / OAuth2** | Authentication |
| **PostgreSQL / SQLite** | Databases |
| **Docker** | Containerization |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ and ⚡ FastAPI

**[⭐ Star this repo](https://github.com/YOUR_USERNAME/FAST_API)** if you find it helpful!

</div>
