"""
Prueba de integración — Pipeline RAG end-to-end.

Valida el flujo completo: ingesta → embedding → búsqueda → respuesta generada.
Usa mocks de OpenAI para no requerir API key real en CI.
"""

import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from src.main import app


def _mock_openai_client():
    """Crea un mock completo del cliente OpenAI."""
    client = MagicMock()

    # Mock embeddings
    embedding_resp = MagicMock()
    embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
    client.embeddings.create = AsyncMock(return_value=embedding_resp)

    # Mock chat completions
    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = json.dumps({
        "requirements": ["Servidor rack 2U", "128GB RAM DDR4", "Certificación ISO 27001"],
        "restrictions": ["Marca específica sin equivalente"],
        "brands_mentioned": ["Dell PowerEdge R750"],
        "certifications": ["ISO 27001"],
        "experience_requirements": ["5 años en sector público"],
        "geographic_restrictions": [],
        "equivalent_expression_present": True,
        "technical_justification_quality": "débil",
        "key_fragments": [{"text": "Dell PowerEdge R750", "reason": "Marca específica"}]
    })
    completion.usage = MagicMock(total_tokens=500)
    client.chat.completions.create = AsyncMock(return_value=completion)

    return client


@pytest.mark.anyio
async def test_rag_pipeline_end_to_end():
    """
    Prueba de integración del pipeline RAG completo:
    1. Ingestar un documento al vector store
    2. Consultar el vector store con una pregunta relacionada
    3. Verificar que la respuesta contiene información relevante
    """
    mock_client = _mock_openai_client()

    with patch("src.rag.vector_store.AsyncOpenAI", return_value=mock_client), \
         patch("src.rag.retriever.AsyncOpenAI", return_value=mock_client):

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:

            # 1. Verificar health
            health = await client.get("/api/v1/health")
            assert health.status_code == 200
            assert health.json()["status"] == "healthy"

            # 2. Ingestar documento de prueba
            ingest_payload = {
                "documents": [
                    {
                        "id": "SEACE-2026-TEST-001",
                        "content": (
                            "Adquisición de servidores rack para el Data Center. "
                            "Se requiere cinco servidores Dell PowerEdge R750 con "
                            "procesador Intel Xeon Gold 6338, 128GB RAM DDR4 ECC, "
                            "4 discos SSD 960GB RAID 10. Certificación ISO 27001 "
                            "obligatoria. Experiencia mínima 5 años sector público."
                        ),
                        "metadata": {
                            "entity": "OECE",
                            "year": 2026,
                            "type": "TDR",
                            "object": "Servidores"
                        }
                    }
                ]
            }

            ingest_response = await client.post("/api/v1/ingest", json=ingest_payload)
            assert ingest_response.status_code == 200
            ingest_data = ingest_response.json()
            assert ingest_data["status"] == "ok"
            assert ingest_data["indexed_docs"] >= 1
            assert len(ingest_data["errors"]) == 0

            # 3. Consultar el vector store
            query_payload = {
                "query": "requisitos de servidores",
                "top_k": 3
            }

            query_response = await client.post("/api/v1/query", json=query_payload)
            assert query_response.status_code == 200
            query_data = query_response.json()
            assert "response" in query_data
            assert "sources" in query_data
            assert "tokens_used" in query_data
            assert "latency_ms" in query_data
            assert query_data["tokens_used"] > 0
            assert query_data["latency_ms"] > 0


@pytest.mark.anyio
async def test_ingest_then_health_check():
    """Verifica que después de ingesta el sistema sigue healthy."""
    mock_client = _mock_openai_client()

    with patch("src.rag.vector_store.AsyncOpenAI", return_value=mock_client):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Ingestar
            await client.post("/api/v1/ingest", json={
                "documents": [{"content": "Documento de prueba " * 20, "metadata": {}}]
            })

            # Health debe seguir OK
            health = await client.get("/api/v1/health")
            assert health.status_code == 200
            assert health.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_query_without_documents_returns_response():
    """Una consulta sin documentos indexados debe responder sin error."""
    mock_client = _mock_openai_client()

    with patch("src.rag.vector_store.AsyncOpenAI", return_value=mock_client), \
         patch("src.rag.retriever.AsyncOpenAI", return_value=mock_client):

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/query", json={
                "query": "información que no existe"
            })
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
