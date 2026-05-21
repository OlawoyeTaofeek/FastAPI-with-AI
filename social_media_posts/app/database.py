from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(
    bind=engine, autoflush=False,autocommit=False
)

Base = declarative_base()

def get_db():
    db = sessionLocal()

    try:
        yield db 
    finally:
        db.close()

# def get_db():
#     with sessionLocal() as db:
#         yield db  Context manager approach