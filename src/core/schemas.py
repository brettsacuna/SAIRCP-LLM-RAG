"""Esquemas de datos del sistema SAIRCP."""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


# --- Enums ---

class RiskLevel(str, Enum):
    LOW = "BAJO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"


class DocumentType(str, Enum):
    TDR = "TDR"
    BASES = "BASES_ADMINISTRATIVAS"
    EETT = "ESPECIFICACIONES_TECNICAS"
    ESTUDIO_MERCADO = "ESTUDIO_MERCADO"


# --- Request Models ---

class AnalyzeDocumentRequest(BaseModel):
    """Solicitud de análisis de documento."""
    content: str = Field(..., min_length=50, description="Contenido del documento a analizar")
    document_type: DocumentType = Field(..., description="Tipo de documento")
    process_id: Optional[str] = Field(None, description="ID del proceso SEACE asociado")
    entity_name: Optional[str] = Field(None, description="Nombre de la entidad contratante")


class IngestDocumentRequest(BaseModel):
    """Solicitud de ingesta de documentos al vector store."""
    documents: List[dict] = Field(..., description="Lista de documentos con content y metadata")
    collection: Optional[str] = Field(None, description="Colección destino")


class QueryRequest(BaseModel):
    """Consulta de lenguaje natural al sistema."""
    query: str = Field(..., min_length=5)
    session_id: Optional[str] = None
    top_k: Optional[int] = Field(5, ge=1, le=20)


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
    indicators: List[RiskIndicator]
    document_fragment: str
    recommendation: str


class AnalysisResult(BaseModel):
    """Resultado completo del análisis de riesgo."""
    analysis_id: str
    timestamp: datetime
    document_type: DocumentType
    total_score: int
    risk_level: RiskLevel
    alerts: List[AlertDetail]
    summary: str
    requirements_found: List[str]
    potential_restrictions: List[str]
    comparable_processes: List[dict]
    providers_found: List[dict]
    processing_time_ms: float
    model_used: str
    trace_id: str


class IngestResponse(BaseModel):
    status: str
    indexed_docs: int
    errors: List[str]


class QueryResponse(BaseModel):
    response: str
    sources: List[dict]
    tokens_used: int
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
    components: dict
    timestamp: datetime
