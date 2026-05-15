<div align="center">

# 🤖 End-to-End ML with FastAPI

**Train, serve, and monitor machine learning models via a REST API**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

[← Back to Series](../README.md)

</div>

---

## 📌 About

This project bridges the gap between data science and backend engineering. You'll build a complete ML pipeline — from training a model to exposing it through a FastAPI service — covering everything MLEs and backend devs need to collaborate effectively.

## ✨ Features

- 🧠 Train and persist ML models
- 🔮 Real-time prediction endpoints
- ⚙️ Background training jobs
- 📊 Model performance metrics
- 🔀 Multiple model version support
- 🐳 Docker-ready for deployment

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ML | Scikit-learn / PyTorch |
| Task Queue | Celery + Redis |
| Model Storage | Joblib / MLflow |
| Containerization | Docker |
| Monitoring | Prometheus (optional) |

## 🚀 Getting Started

```bash
cd EndToEndMLWithFastAPI
uv sync
uv run uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/train` | Trigger model training |
| `POST` | `/predict` | Get a prediction |
| `GET` | `/models` | List available models |
| `GET` | `/models/{id}/metrics` | View model performance |
| `POST` | `/models/{id}/activate` | Switch active model |

## 💡 Key Concepts Covered

- Loading and saving ML models with joblib/pickle
- Background task execution with Celery
- Input validation for ML features using Pydantic
- Model versioning and A/B testing patterns
- Dockerizing a FastAPI + ML app
- Async vs sync endpoints for CPU-bound tasks
