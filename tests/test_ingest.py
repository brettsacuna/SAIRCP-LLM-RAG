"""Pruebas unitarias — Pipeline de ingesta y chunking."""

import pytest
from src.rag.ingest import IngestPipeline
from src.core.config import settings
from unittest.mock import AsyncMock, MagicMock


class TestChunking:
    """Valida la lógica de chunking de documentos."""

    def _make_pipeline(self):
        mock_vs = MagicMock()
        mock_vs.add = AsyncMock()
        return IngestPipeline(vector_store=mock_vs)

    def test_short_text_produces_one_chunk(self):
        pipeline = self._make_pipeline()
        chunks = pipeline._chunk_text("Texto corto de prueba.")
        assert len(chunks) == 1

    def test_chunk_size_respected(self):
        pipeline = self._make_pipeline()
        text = "a" * 2500
        chunks = pipeline._chunk_text(text)
        for chunk in chunks:
            assert len(chunk) <= settings.CHUNK_SIZE

    def test_overlap_produces_more_chunks(self):
        pipeline = self._make_pipeline()
        text = "a" * 2000
        chunks = pipeline._chunk_text(text)
        # Con chunk_size=1000 y overlap=200, 2000 chars -> 3 chunks aprox
        assert len(chunks) >= 2

    def test_empty_text_produces_one_chunk(self):
        pipeline = self._make_pipeline()
        chunks = pipeline._chunk_text("")
        assert len(chunks) == 1

    def test_exact_chunk_size(self):
        pipeline = self._make_pipeline()
        text = "a" * settings.CHUNK_SIZE
        chunks = pipeline._chunk_text(text)
        assert len(chunks) == 1


class TestDocumentProcessor:
    """Valida la extracción de texto de documentos."""

    def test_extract_text_rejects_unsupported_type(self):
        from src.rag.document_processor import extract_text
        with pytest.raises(ValueError, match="Tipo no soportado"):
            extract_text(b"data", "text/plain")

    def test_extract_text_accepts_pdf_type(self):
        from src.rag.document_processor import extract_text
        # Un PDF inválido debe fallar en extracción, no en validación de tipo
        try:
            extract_text(b"%PDF-1.4 invalid", "application/pdf")
        except Exception as e:
            assert "Tipo no soportado" not in str(e)


class TestConfigSettings:
    """Valida la configuración del sistema."""

    def test_chunk_size_is_positive(self):
        assert settings.CHUNK_SIZE > 0

    def test_chunk_overlap_less_than_size(self):
        assert settings.CHUNK_OVERLAP < settings.CHUNK_SIZE

    def test_top_k_is_reasonable(self):
        assert 1 <= settings.TOP_K <= 20

    def test_similarity_threshold_in_range(self):
        assert 0.0 < settings.SIMILARITY_THRESHOLD <= 1.0

    def test_score_thresholds_ordered(self):
        assert settings.SCORE_THRESHOLD_LOW < settings.SCORE_THRESHOLD_MEDIUM

    def test_openai_temperature_is_zero(self):
        assert settings.OPENAI_TEMPERATURE == 0.0
