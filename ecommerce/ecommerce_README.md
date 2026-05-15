<div align="center">

# 🛒 E-Commerce API

**A scalable product & order management backend built with FastAPI**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)

[← Back to Series](../README.md)

</div>

---

## 📌 About

The E-Commerce API project simulates a real online store backend. You'll learn how to handle complex relational data (products, carts, orders), implement role-based access control, and integrate third-party payment services.

## ✨ Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart management
- 📦 Order creation and tracking
- 💳 Payment integration (Stripe-ready)
- 👥 Role-based access (Admin / Customer)
- 🔍 Search, filter, and pagination

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Caching | Redis |
| Payments | Stripe SDK |
| Auth | JWT / OAuth2 |

## 🚀 Getting Started

```bash
cd ecommerce
uv sync
# Configure .env (DB, Stripe keys)
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | List products |
| `POST` | `/products` | Create product (Admin) |
| `GET` | `/products/{id}` | Get product detail |
| `POST` | `/cart/add` | Add item to cart |
| `GET` | `/cart` | View current cart |
| `POST` | `/orders` | Place an order |
| `GET` | `/orders/{id}` | Track an order |
| `POST` | `/payments/checkout` | Initiate payment |

## 💡 Key Concepts Covered

- Many-to-many relationships (Products ↔ Categories)
- Cart logic and inventory checks
- Role-based dependency guards
- Database transactions for order integrity
- Stripe webhook handling
- Redis caching for product listings
