"""Fixtures compartidos para todas las pruebas."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.core.config import settings


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Cliente HTTP de prueba contra la app FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def mock_openai():
    """Mock del cliente OpenAI para pruebas sin llamadas reales."""
    with patch("openai.AsyncOpenAI") as mock:
        instance = mock.return_value

        # Mock chat completions
        completion = MagicMock()
        completion.choices = [MagicMock()]
        completion.choices[0].message.content = '{"requirements": ["req1"], "restrictions": [], "brands_mentioned": [], "certifications": [], "experience_requirements": [], "geographic_restrictions": [], "equivalent_expression_present": true, "technical_justification_quality": "fuerte", "key_fragments": []}'
        completion.usage = MagicMock(total_tokens=150)
        instance.chat.completions.create = AsyncMock(return_value=completion)

        # Mock embeddings
        embedding_resp = MagicMock()
        embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
        instance.embeddings.create = AsyncMock(return_value=embedding_resp)

        yield instance


@pytest.fixture
def sample_tdr_content():
    """Contenido de ejemplo de un TDR para pruebas."""
    return """
    TÉRMINOS DE REFERENCIA
    Adquisición de Servidores para el Data Center Institucional

    1. OBJETO DE LA CONTRATACIÓN
    Adquisición de cinco (5) servidores de rack Dell PowerEdge R750 con procesador
    Intel Xeon Gold 6338 de 2.0GHz, 32 cores, para el Data Center principal.

    2. REQUISITOS TÉCNICOS MÍNIMOS
    - Servidor tipo rack 2U
    - Marca Dell PowerEdge R750 o equivalente
    - Procesador Intel Xeon Gold 6338 o superior
    - Memoria RAM: 128GB DDR4 ECC mínimo
    - Almacenamiento: 4 discos SSD de 960GB en RAID 10
    - Certificación ISO 27001 del proveedor
    - Garantía mínima de 3 años on-site

    3. EXPERIENCIA DEL POSTOR
    El postor deberá acreditar experiencia mínima de 5 años en venta de equipos
    de cómputo al sector público, con un monto facturado no menor a 3 veces
    el valor referencial.

    4. PLAZO DE ENTREGA
    Treinta (30) días calendario contados desde la suscripción del contrato.
    """


@pytest.fixture
def sample_analysis_result():
    """Resultado de análisis de ejemplo para pruebas."""
    return {
        "analysis_id": "ANA-test001",
        "timestamp": "2026-04-06T15:30:00Z",
        "document_type": "TDR",
        "total_score": 65,
        "risk_level": "ALTO",
        "alerts": [
            {
                "alert_id": "ALT-test001-001",
                "description": "Mención explícita de marca",
                "severity": "ALTO",
                "indicators": [
                    {"indicator": "brand_explicit", "category": "reglas_deterministicas",
                     "weight": 20, "evidence": "Dell PowerEdge R750", "source": "regla"}
                ],
                "document_fragment": "servidores Dell PowerEdge R750",
                "recommendation": "Incluir expresión 'o equivalente'"
            }
        ],
        "summary": "El documento presenta riesgo ALTO.",
        "requirements_found": ["Servidor rack 2U", "128GB RAM"],
        "potential_restrictions": ["Marca específica"],
        "comparable_processes": [],
        "providers_found": [],
        "processing_time_ms": 12450.5,
        "model_used": "gpt-4o",
        "trace_id": "test-trace-id"
    }
