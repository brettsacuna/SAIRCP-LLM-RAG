"""Endpoints REST del sistema SAIRCP."""

import time
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from src.core.schemas import (
    AnalyzeDocumentRequest, AnalysisResult, IngestDocumentRequest,
    IngestResponse, QueryRequest, QueryResponse, HealthResponse,
)
from src.core.config import settings
from src.agents.orchestrator import AgentOrchestrator
from src.rag.ingest import IngestPipeline
from src.rag.retriever import RAGRetriever

router = APIRouter()


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
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/analyze", response_model=AnalysisResult, tags=["Análisis"])
async def analyze_document(req: AnalyzeDocumentRequest, request: Request):
    """
    Analiza un documento de contratación pública y genera
    un informe de riesgos con scoring y evidencia trazable.
    """
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
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

    elapsed = (time.perf_counter() - start) * 1000
    result.processing_time_ms = elapsed
    return result


@router.post("/analyze/upload", response_model=AnalysisResult, tags=["Análisis"])
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    request: Request = None,
):
    """Carga un PDF/DOCX y ejecuta el análisis de riesgo."""
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(400, "Solo se aceptan archivos PDF o DOCX.")

    content_bytes = await file.read()
    # Extracción de texto según tipo
    from src.rag.document_processor import extract_text
    text = extract_text(content_bytes, file.content_type)

    orchestrator = AgentOrchestrator(
        vector_store=request.app.state.vector_store
    )
    start = time.perf_counter()
    result = await orchestrator.analyze(content=text, document_type="TDR")
    result.processing_time_ms = (time.perf_counter() - start) * 1000
    return result


@router.post("/ingest", response_model=IngestResponse, tags=["Ingesta"])
async def ingest_documents(req: IngestDocumentRequest, request: Request):
    """Ingesta documentos al vector store para búsqueda RAG."""
    pipeline = IngestPipeline(vector_store=request.app.state.vector_store)
    try:
        count, errors = await pipeline.ingest(req.documents, req.collection)
        return IngestResponse(status="ok", indexed_docs=count, errors=errors)
    except Exception as e:
        raise HTTPException(500, f"Error en ingesta: {str(e)}")


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
        raise HTTPException(500, f"Error en consulta: {str(e)}")

    return QueryResponse(
        response=answer,
        sources=sources,
        tokens_used=tokens,
        latency_ms=(time.perf_counter() - start) * 1000,
    )
