from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from core.database import engine, Base
from core.redis import redis_client
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up....")

    await init_database()
    await init_redis()

    print("All systems ready")
    yield
    print("Shutting down...")

    await engine.dispose()
    await redis_client.aclose()

    print("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

async def init_database():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        print("Database Connected")

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        print("Database tables ready")

    except Exception as e:  
        print(f"Database failed: {e}")
        raise 

async def init_redis():
    try:
        await redis_client.ping()
        print("Redis connected")
        # 2. Check memory usage — warn if Redis is near its limit
        info = await redis_client.info("memory")
        used = info["used_memory_human"]
        peak = info["used_memory_peak_human"]
        print(f"  ✓ Redis memory — used: {used}, peak: {peak}")

    except Exception as e:
        print(f"  ✗ Redis failed: {e}")
        raise
