"""
inkwell/database.py
─────────────────────────────────────────────────────────────────────────────
Async SQLAlchemy engine + session factory for FastAPI dependency injection.

Requirements
────────────
    pip install sqlalchemy[asyncio] asyncpg alembic python-dotenv

Usage in FastAPI
────────────────
    from database import get_db

    @app.get("/posts")
    async def list_posts(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Post))
        return result.scalars().all()
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from models import Base

load_dotenv()

# ── Engine ────────────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/inkwell",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,          # detect stale connections
    pool_recycle=1800,           # recycle connections every 30 min
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,      # avoid lazy-load surprises after commit
    autoflush=False,
    autocommit=False,
)


# ── FastAPI dependency ────────────────────────────────────────────────────────


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a database session and guarantees cleanup.

    Use as a FastAPI dependency:
        db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Table creation (dev / tests only) ────────────────────────────────────────


async def create_all_tables() -> None:
    """
    Create all tables from metadata.
    In production, use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    """Drop all tables. Used in test teardown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ── Alembic target metadata ───────────────────────────────────────────────────
# Referenced in alembic/env.py:
#   from database import target_metadata
target_metadata = Base.metadata
