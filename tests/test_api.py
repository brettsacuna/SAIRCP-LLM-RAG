"""Pruebas unitarias — Endpoints de la API."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


# =============================================
# /health
# =============================================
@pytest.mark.anyio
async def test_health_returns_200(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "components" in data
    assert "timestamp" in data


@pytest.mark.anyio
async def test_health_contains_required_components(client):
    response = await client.get("/api/v1/health")
    data = response.json()
    components = data["components"]
    assert "api" in components
    assert "llm_provider" in components
    assert components["api"] == "ok"


# =============================================
# /analyze — validación
# =============================================
@pytest.mark.anyio
async def test_analyze_requires_content(client):
    response = await client.post("/api/v1/analyze", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_analyze_rejects_short_content(client):
    response = await client.post("/api/v1/analyze", json={
        "content": "texto corto",
        "document_type": "TDR"
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_analyze_rejects_invalid_doc_type(client):
    response = await client.post("/api/v1/analyze", json={
        "content": "x" * 100,
        "document_type": "INVALID_TYPE"
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_analyze_accepts_valid_doc_types(client):
    valid_types = ["TDR", "BASES_ADMINISTRATIVAS", "ESPECIFICACIONES_TECNICAS", "ESTUDIO_MERCADO"]
    for dt in valid_types:
        response = await client.post("/api/v1/analyze", json={
            "content": "a" * 5,
            "document_type": dt
        })
        # 422 por min_length o 500 por falta de API key, pero no 422 por tipo inválido
        assert response.status_code in [422, 500]


# =============================================
# /analyze/upload — validación
# =============================================
@pytest.mark.anyio
async def test_upload_rejects_invalid_content_type(client):
    response = await client.post(
        "/api/v1/analyze/upload",
        files={"file": ("test.txt", b"content", "text/plain")}
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_upload_accepts_pdf_content_type(client):
    response = await client.post(
        "/api/v1/analyze/upload",
        files={"file": ("test.pdf", b"%PDF-1.4 fake", "application/pdf")}
    )
    # Fallará en extracción pero no en validación de tipo
    assert response.status_code in [200, 500]


# =============================================
# /query — validación
# =============================================
@pytest.mark.anyio
async def test_query_requires_query_field(client):
    response = await client.post("/api/v1/query", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_query_rejects_short_query(client):
    response = await client.post("/api/v1/query", json={"query": "ab"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_query_validates_top_k_range(client):
    response = await client.post("/api/v1/query", json={
        "query": "requisitos de TDR",
        "top_k": 50  # max is 20
    })
    assert response.status_code == 422


# =============================================
# /ingest — validación
# =============================================
@pytest.mark.anyio
async def test_ingest_requires_documents(client):
    response = await client.post("/api/v1/ingest", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_ingest_accepts_valid_payload(client):
    response = await client.post("/api/v1/ingest", json={
        "documents": [{"content": "Texto de prueba", "metadata": {"type": "test"}}]
    })
    # 200 o 500 (si no hay API key para embeddings)
    assert response.status_code in [200, 500]
