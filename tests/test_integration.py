"""
Prueba de integración — Pipeline RAG end-to-end.
Usa mocks de OpenAI para no requerir API key real en CI.
"""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient, ASGITransport
from src.main import app
from src.rag.vector_store import VectorStoreManager


def _setup_app_with_mocks():
    """Configura app.state.vector_store con mocks para CI."""
    mock_openai = MagicMock()

    # Mock embeddings
    embedding_resp = MagicMock()
    embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_openai.embeddings.create = AsyncMock(return_value=embedding_resp)

    # Mock chat completions
    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = json.dumps({
        "requirements": ["Servidor rack 2U", "128GB RAM DDR4"],
        "restrictions": ["Marca específica"],
        "brands_mentioned": ["Dell PowerEdge R750"],
        "certifications": ["ISO 27001"],
        "experience_requirements": ["5 años"],
        "geographic_restrictions": [],
        "equivalent_expression_present": True,
        "technical_justification_quality": "débil",
        "key_fragments": []
    })
    completion.usage = MagicMock(total_tokens=500)
    mock_openai.chat.completions.create = AsyncMock(return_value=completion)

    # Real ChromaDB en memoria temporal
    vs = VectorStoreManager()
    vs.openai = mock_openai

    import chromadb
    vs.client = chromadb.Client()
    vs.collection = vs.client.get_or_create_collection(
        name="test_integration",
        metadata={"hnsw:space": "cosine"},
    )

    app.state.vector_store = vs
    return mock_openai


@pytest.mark.anyio
async def test_rag_pipeline_end_to_end():
    """Pipeline completo: health → ingest → query."""
    mock_openai = _setup_app_with_mocks()

    with patch("src.rag.retriever.AsyncOpenAI", return_value=mock_openai):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Health
            health = await client.get("/api/v1/health")
            assert health.status_code == 200
            assert health.json()["status"] == "healthy"

            # 2. Ingest
            ingest_response = await client.post("/api/v1/ingest", json={
                "documents": [{
                    "id": "TEST-001",
                    "content": "Adquisición de servidores Dell PowerEdge R750 con procesador Intel Xeon Gold.",
                    "metadata": {"entity": "OECE", "type": "TDR"}
                }]
            })
            assert ingest_response.status_code == 200
            assert ingest_response.json()["status"] == "ok"
            assert ingest_response.json()["indexed_docs"] >= 1

            # 3. Query
            query_response = await client.post("/api/v1/query", json={
                "query": "requisitos servidores", "top_k": 3
            })
            assert query_response.status_code == 200
            qdata = query_response.json()
            assert "response" in qdata
            assert "sources" in qdata
            assert qdata["tokens_used"] > 0


@pytest.mark.anyio
async def test_ingest_then_health_stays_healthy():
    """Después de ingesta, el sistema sigue healthy."""
    _setup_app_with_mocks()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/ingest", json={
            "documents": [{"content": "Documento de prueba " * 20, "metadata": {}}]
        })
        health = await client.get("/api/v1/health")
        assert health.status_code == 200
        assert health.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_query_empty_vectorstore():
    """Query sobre vector store vacío retorna respuesta sin error."""
    mock_openai = _setup_app_with_mocks()

    # Limpiar collection
    app.state.vector_store.collection = app.state.vector_store.client.get_or_create_collection(
        name="test_empty", metadata={"hnsw:space": "cosine"}
    )

    with patch("src.rag.retriever.AsyncOpenAI", return_value=mock_openai):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/query", json={"query": "información inexistente"})
            assert response.status_code == 200
            assert "response" in response.json()


@pytest.mark.anyio
async def test_history_endpoint_after_operations():
    """El endpoint /history refleja las operaciones realizadas."""
    _setup_app_with_mocks()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/history")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert isinstance(data["results"], list)
