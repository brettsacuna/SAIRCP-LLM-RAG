"""Esquemas de datos del sistema SAIRCP."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


# --- Enums ---

class RiskLevel(StrEnum):
    LOW = "BAJO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"


class DocumentType(StrEnum):
    TDR = "TDR"
    BASES = "BASES_ADMINISTRATIVAS"
    EETT = "ESPECIFICACIONES_TECNICAS"
    ESTUDIO_MERCADO = "ESTUDIO_MERCADO"


# --- Request Models ---

class AnalyzeDocumentRequest(BaseModel):
    """Solicitud de análisis de documento."""
    content: str = Field(..., min_length=50, description="Contenido del documento a analizar")
    document_type: DocumentType = Field(..., description="Tipo de documento")
    process_id: str | None = Field(None, description="ID del proceso SEACE asociado")
    entity_name: str | None = Field(None, description="Nombre de la entidad contratante")


class IngestDocumentRequest(BaseModel):
    """Solicitud de ingesta de documentos al vector store."""
    documents: list[dict] = Field(..., description="Lista de documentos con content y metadata")
    collection: str | None = Field(None, description="Colección destino")


class QueryRequest(BaseModel):
    """Consulta de lenguaje natural al sistema."""
    query: str = Field(..., min_length=5)
    session_id: str | None = None
    top_k: int | None = Field(5, ge=1, le=20)


# --- Response Models ---

class RiskIndicator(BaseModel):
    """Indicador de riesgo detectado."""
    indicator: str
    category: str
    weight: int
    evidence: str
    source: str


class AlertDetail(BaseModel):
    """Detalle de una alerta generada."""
    alert_id: str
    description: str
    severity: RiskLevel
    indicators: list[RiskIndicator]
    document_fragment: str
    recommendation: str


class AnalysisResult(BaseModel):
    """Resultado completo del análisis de riesgo."""
    analysis_id: str
    timestamp: datetime
    document_type: DocumentType
    total_score: int
    risk_level: RiskLevel
    alerts: list[AlertDetail]
    summary: str
    requirements_found: list[str]
    potential_restrictions: list[str]
    comparable_processes: list[dict]
    providers_found: list[dict]
    processing_time_ms: float
    model_used: str
    trace_id: str


class IngestResponse(BaseModel):
    status: str
    indexed_docs: int
    errors: list[str]


class QueryResponse(BaseModel):
    response: str
    sources: list[dict]
    tokens_used: int
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
    components: dict
    timestamp: datetime
