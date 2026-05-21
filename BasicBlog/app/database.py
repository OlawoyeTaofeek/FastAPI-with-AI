from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base # old method

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()
    try:
        yield db 
    except:
        db.rollback()
        raise 
    finally:
        db.close()