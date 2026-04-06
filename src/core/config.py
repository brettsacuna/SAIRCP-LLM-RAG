"""Configuración central del sistema SAIRCP."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Variables de entorno y configuración."""

    # --- App ---
    APP_NAME: str = "SAIRCP-LLM-RAG"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # --- OpenAI ---
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_TEMPERATURE: float = 0.0
    OPENAI_MAX_TOKENS: int = 4096

    # --- RAG ---
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.75

    # --- ChromaDB ---
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    CHROMA_COLLECTION_NAME: str = "saircp_documents"

    # --- PostgreSQL ---
    DATABASE_URL: str = "postgresql://saircp:saircp_pass@localhost:5432/saircp_db"

    # --- Seguridad ---
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # --- Scoring ---
    SCORE_THRESHOLD_LOW: int = 30
    SCORE_THRESHOLD_MEDIUM: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
