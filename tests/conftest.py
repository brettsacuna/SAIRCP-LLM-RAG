"""Fixtures compartidos para todas las pruebas."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient, ASGITransport
from src.main import app
from src.rag.vector_store import VectorStoreManager


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Cliente HTTP de prueba con vector_store inicializado."""
    # Inicializar vector_store en app.state para que los endpoints funcionen
    vs = VectorStoreManager()
    vs.client = MagicMock()
    vs.collection = MagicMock()
    vs.collection.count.return_value = 0
    vs.collection.add = MagicMock()
    vs.openai = MagicMock()

    # Mock de embeddings
    embedding_resp = MagicMock()
    embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
    vs.openai.embeddings.create = AsyncMock(return_value=embedding_resp)

    app.state.vector_store = vs

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def mock_openai_client():
    """Mock completo del cliente OpenAI."""
    client = MagicMock()

    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = '{"requirements": ["req1"], "restrictions": [], "brands_mentioned": [], "certifications": [], "experience_requirements": [], "geographic_restrictions": [], "equivalent_expression_present": true, "technical_justification_quality": "fuerte", "key_fragments": []}'
    completion.usage = MagicMock(total_tokens=150)
    client.chat.completions.create = AsyncMock(return_value=completion)

    embedding_resp = MagicMock()
    embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
    client.embeddings.create = AsyncMock(return_value=embedding_resp)

    return client


@pytest.fixture
def sample_tdr_content():
    """Contenido TDR de ejemplo para pruebas."""
    return (
        "TÉRMINOS DE REFERENCIA - Adquisición de Servidores para el Data Center.\n"
        "Se requiere la adquisición de cinco (5) servidores Dell PowerEdge R750 "
        "con procesador Intel Xeon Gold 6338 de 2.0GHz, 32 cores.\n"
        "Memoria RAM: 128GB DDR4 ECC mínimo.\n"
        "Almacenamiento: 4 discos SSD de 960GB en RAID 10.\n"
        "Certificación ISO 27001 del proveedor.\n"
        "Experiencia mínima de 5 años en sector público.\n"
        "Plazo de entrega: 30 días calendario."
    )
