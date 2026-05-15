from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str
    database_host: str
    database_username: str
    database_name: str
    database_port: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()