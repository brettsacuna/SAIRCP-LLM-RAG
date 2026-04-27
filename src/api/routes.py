"""Endpoints REST del sistema SAIRCP."""

import time
from datetime import UTC, datetime

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from src.agents.orchestrator import AgentOrchestrator
from src.core.config import settings
from src.core.schemas import (
    AnalysisResult,
    AnalyzeDocumentRequest,
    HealthResponse,
    IngestDocumentRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from src.rag.ingest import IngestPipeline
from src.rag.retriever import RAGRetriever

router = APIRouter()

# In-memory storage for analysis history
_analysis_history: list[dict] = []


@router.get("/health", response_model=HealthResponse, tags=["Sistema"])
async def health_check(request: Request):
    """Health check del sistema y sus componentes."""
    vs = getattr(request.app.state, "vector_store", None)
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        components={
            "api": "ok",
            "vector_store": "ok" if vs else "not_initialized",
            "llm_provider": "openai",
        },
        timestamp=datetime.now(UTC),
    )


@router.post("/analyze", response_model=AnalysisResult, tags=["Análisis"])
async def analyze_document(req: AnalyzeDocumentRequest, request: Request):
    """Analiza un documento de contratación pública y genera un informe de riesgos."""
    start = time.perf_counter()
    orchestrator = AgentOrchestrator(
        vector_store=request.app.state.vector_store
    )
    try:
        result = await orchestrator.analyze(
            content=req.content,
            document_type=req.document_type,
            process_id=req.process_id,
            entity_name=req.entity_name,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {e!s}") from e

    elapsed = (time.perf_counter() - start) * 1000
    result.processing_time_ms = elapsed

    # Almacenar resultado en historial
    _analysis_history.append(result.model_dump(mode="json"))

    return result


@router.post("/analyze/upload", response_model=AnalysisResult, tags=["Análisis"])
async def analyze_uploaded_file(
    request: Request,
    file: UploadFile = File(...),  # noqa: B008
):
    """Carga un PDF/DOCX y ejecuta el análisis de riesgo."""
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(400, "Solo se aceptan archivos PDF o DOCX.")

    content_bytes = await file.read()
    from src.rag.document_processor import extract_text
    try:
        text = extract_text(content_bytes, file.content_type)
    except Exception as e:
        raise HTTPException(500, f"Error extrayendo texto: {e!s}") from e

    orchestrator = AgentOrchestrator(
        vector_store=request.app.state.vector_store
    )
    start = time.perf_counter()
    try:
        result = await orchestrator.analyze(content=text, document_type="TDR")
    except Exception as e:
        raise HTTPException(500, f"Error en análisis: {e!s}") from e
    result.processing_time_ms = (time.perf_counter() - start) * 1000
    _analysis_history.append(result.model_dump(mode="json"))
    return result


@router.post("/ingest", response_model=IngestResponse, tags=["Ingesta"])
async def ingest_documents(req: IngestDocumentRequest, request: Request):
    """Ingesta documentos al vector store para búsqueda RAG."""
    pipeline = IngestPipeline(vector_store=request.app.state.vector_store)
    try:
        count, errors = await pipeline.ingest(req.documents, req.collection)
        return IngestResponse(status="ok", indexed_docs=count, errors=errors)
    except Exception as e:
        raise HTTPException(500, f"Error en ingesta: {e!s}") from e


@router.post("/query", response_model=QueryResponse, tags=["Consulta"])
async def query_rag(req: QueryRequest, request: Request):
    """Consulta de lenguaje natural con contexto RAG."""
    start = time.perf_counter()
    retriever = RAGRetriever(vector_store=request.app.state.vector_store)
    try:
        answer, sources, tokens = await retriever.query(
            query=req.query, top_k=req.top_k
        )
    except Exception as e:
        raise HTTPException(500, f"Error en consulta: {e!s}") from e

    return QueryResponse(
        response=answer,
        sources=sources,
        tokens_used=tokens,
        latency_ms=(time.perf_counter() - start) * 1000,
    )


@router.get("/history", tags=["Historial"])
async def get_analysis_history():
    """Retorna el historial de análisis realizados."""
    return {"total": len(_analysis_history), "results": _analysis_history[-50:]}
