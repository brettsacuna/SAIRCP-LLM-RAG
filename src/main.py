"""
SAIRCP-LLM-RAG: Sistema de Apoyo para Identificación de Riesgos
en Contrataciones Públicas mediante IA.

Extensión del SEACE 4.0 — OECE
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.routes import router as api_router
from src.core.config import settings
from src.rag.vector_store import VectorStoreManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa y limpia recursos al inicio/fin de la app."""
    # Startup
    app.state.vector_store = VectorStoreManager()
    await app.state.vector_store.initialize()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="SAIRCP-LLM-RAG API",
    description=(
        "Sistema de Apoyo para la Identificación de Riesgos "
        "en Contrataciones Públicas mediante IA — Extensión SEACE 4.0"
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
