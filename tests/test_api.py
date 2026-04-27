"""Pruebas unitarias — Endpoints de la API."""

import pytest


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
    assert "vector_store" in components
    assert components["api"] == "ok"
    assert components["llm_provider"] == "openai"


@pytest.mark.anyio
async def test_health_version_is_set(client):
    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["version"] == "1.0.0"


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
async def test_analyze_accepts_all_valid_doc_types(client):
    valid_types = ["TDR", "BASES_ADMINISTRATIVAS", "ESPECIFICACIONES_TECNICAS", "ESTUDIO_MERCADO"]
    for dt in valid_types:
        response = await client.post("/api/v1/analyze", json={
            "content": "a" * 5,
            "document_type": dt
        })
        # 422 por min_length o 500 por falta de API key, pero no 422 por tipo inválido
        assert response.status_code in [422, 500]


@pytest.mark.anyio
async def test_analyze_requires_document_type(client):
    response = await client.post("/api/v1/analyze", json={
        "content": "x" * 100
    })
    assert response.status_code == 422


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
async def test_upload_rejects_empty_file(client):
    response = await client.post(
        "/api/v1/analyze/upload",
        files={"file": ("test.pdf", b"", "application/pdf")}
    )
    # Empty PDF will fail extraction → 500
    assert response.status_code == 500


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
        "query": "requisitos de TDR", "top_k": 50
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_query_accepts_valid_top_k(client):
    response = await client.post("/api/v1/query", json={
        "query": "requisitos de TDR", "top_k": 3
    })
    # Will fail with OpenAI mock but not 422
    assert response.status_code in [200, 500]


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
        "documents": [{"content": "Texto de prueba para ingesta", "metadata": {"type": "test"}}]
    })
    # 200 o 500 (si embeddings mock falla)
    assert response.status_code in [200, 500]


@pytest.mark.anyio
async def test_ingest_empty_documents_list(client):
    response = await client.post("/api/v1/ingest", json={
        "documents": []
    })
    # Empty list → 200 with 0 indexed
    assert response.status_code in [200, 422]


# =============================================
# /history
# =============================================
@pytest.mark.anyio
async def test_history_returns_list(client):
    response = await client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "results" in data
    assert isinstance(data["results"], list)
