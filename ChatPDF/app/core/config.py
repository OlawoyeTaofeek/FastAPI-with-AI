# app/core/config.py

# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
from typing import List


class Settings(BaseSettings):

    # -------------------------------------------------------
    # APP
    # -------------------------------------------------------
    APP_NAME: str = "CHATIFY"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"         # development | staging | production
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # -------------------------------------------------------
    # SECURITY
    # -------------------------------------------------------
    SECRET_KEY: str                          
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15   
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     

    # -------------------------------------------------------
    # DATABASE (PostgreSQL - NeonDB)
    # -------------------------------------------------------
    DATABASE_URL: str                        # postgresql+asyncpg://user:pass@host/db
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30

    # -------------------------------------------------------
    # REDIS
    # -------------------------------------------------------
    REDIS_URL: str                           
    REDIS_TTL_REFRESH_TOKEN: int = 604800   
    REDIS_TTL_EMAIL_VERIFY: int = 86400     
    REDIS_TTL_PASSWORD_RESET: int = 3600   
    REDIS_TTL_RATE_LIMIT: int = 60        

    # -------------------------------------------------------
    # EMAIL (Resend / SendGrid)
    # -------------------------------------------------------
    EMAIL_PROVIDER: str = "resend"          # resend | sendgrid | smtp
    EMAIL_API_KEY: str
    EMAIL_FROM_ADDRESS: str
    EMAIL_FROM_NAME: str = "PDF Chat"

    # -------------------------------------------------------
    # AWS S3
    # -------------------------------------------------------
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET_NAME: str
    AWS_S3_PRESIGNED_URL_EXPIRE: int = 3600  

    # -------------------------------------------------------
    # PINECONE
    # -------------------------------------------------------
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str              
    PINECONE_INDEX_NAME: str = "pdf-chat"
    PINECONE_DIMENSION: int = 1536          # OpenAI text-embedding-ada-002

    # -------------------------------------------------------
    # OPENAI
    # -------------------------------------------------------
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.0         # 0 = factual, no hallucination

    # -------------------------------------------------------
    # STRIPE
    # -------------------------------------------------------
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_FREE_PLAN_ID: str = "free"
    STRIPE_PRO_PLAN_PRICE_ID: str

    # -------------------------------------------------------
    # RATE LIMITING (per user)
    # -------------------------------------------------------
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_PDF_SIZE_MB: int = 10
    MAX_PDFS_PER_SESSION: int = 5
    MAX_SESSIONS_PER_USER: int = 20

    # -------------------------------------------------------
    # CORS
    # -------------------------------------------------------
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # -------------------------------------------------------
    # ENVIRONMENT HELPERS
    # -------------------------------------------------------
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def database_url_sync(self) -> str:
        """Sync version for Alembic migrations"""
        return self.DATABASE_URL.replace("asyncpg", "psycopg2")

    # -------------------------------------------------------
    # PYDANTIC CONFIG — reads from .env file
    # -------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Single instance — import this everywhere
settings = Settings()