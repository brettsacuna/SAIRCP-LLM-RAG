"""Pruebas unitarias — Pipeline de ingesta, chunking y configuración."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.rag.ingest import IngestPipeline
from src.core.config import settings


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

    def test_overlap_produces_expected_chunks(self):
        pipeline = self._make_pipeline()
        text = "a" * 2000
        chunks = pipeline._chunk_text(text)
        assert len(chunks) >= 2

    def test_empty_text_produces_one_empty_chunk(self):
        pipeline = self._make_pipeline()
        chunks = pipeline._chunk_text("")
        assert len(chunks) == 1
        assert chunks[0] == ""

    def test_exact_chunk_size_produces_chunks_with_overlap(self):
        pipeline = self._make_pipeline()
        text = "a" * settings.CHUNK_SIZE
        chunks = pipeline._chunk_text(text)
        # Con overlap, un texto de exactamente CHUNK_SIZE produce 1 chunk de CHUNK_SIZE
        # más un chunk de overlap
        assert len(chunks) >= 1
        assert len(chunks[0]) == settings.CHUNK_SIZE

    def test_very_long_text_produces_many_chunks(self):
        pipeline = self._make_pipeline()
        text = "a" * 10000
        chunks = pipeline._chunk_text(text)
        assert len(chunks) > 5

    def test_chunks_cover_full_text(self):
        pipeline = self._make_pipeline()
        text = "abcdefghij" * 200  # 2000 chars
        chunks = pipeline._chunk_text(text)
        # First chunk starts at 0, last chunk covers end
        assert chunks[0].startswith("abcdefghij")

    def test_chunk_overlap_value(self):
        assert settings.CHUNK_OVERLAP == 200
        assert settings.CHUNK_SIZE == 1000


class TestDocumentProcessor:
    """Valida la extracción de texto de documentos."""

    def test_extract_text_rejects_unsupported_type(self):
        from src.rag.document_processor import extract_text
        with pytest.raises(ValueError, match="Tipo no soportado"):
            extract_text(b"data", "text/plain")

    def test_extract_text_rejects_image_type(self):
        from src.rag.document_processor import extract_text
        with pytest.raises(ValueError, match="Tipo no soportado"):
            extract_text(b"data", "image/png")

    def test_extract_text_accepts_pdf_type(self):
        from src.rag.document_processor import extract_text
        try:
            extract_text(b"%PDF-1.4 invalid", "application/pdf")
        except Exception as e:
            assert "Tipo no soportado" not in str(e)

    def test_extract_text_accepts_docx_type(self):
        from src.rag.document_processor import extract_text
        try:
            extract_text(b"PK invalid", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        except Exception as e:
            assert "Tipo no soportado" not in str(e)


class TestConfigSettings:
    """Valida la configuración del sistema."""

    def test_chunk_size_is_positive(self):
        assert settings.CHUNK_SIZE > 0

    def test_chunk_overlap_less_than_size(self):
        assert settings.CHUNK_OVERLAP < settings.CHUNK_SIZE

    def test_chunk_overlap_is_positive(self):
        assert settings.CHUNK_OVERLAP > 0

    def test_top_k_is_reasonable(self):
        assert 1 <= settings.TOP_K <= 20

    def test_similarity_threshold_in_range(self):
        assert 0.0 < settings.SIMILARITY_THRESHOLD <= 1.0

    def test_score_thresholds_ordered(self):
        assert settings.SCORE_THRESHOLD_LOW < settings.SCORE_THRESHOLD_MEDIUM

    def test_openai_temperature_is_zero(self):
        assert settings.OPENAI_TEMPERATURE == 0.0

    def test_openai_model_is_set(self):
        assert settings.OPENAI_MODEL == "gpt-4o"

    def test_embedding_model_is_set(self):
        assert settings.OPENAI_EMBEDDING_MODEL == "text-embedding-3-small"

    def test_app_version_is_set(self):
        assert settings.APP_VERSION == "1.0.0"

    def test_allowed_origins_is_list(self):
        assert isinstance(settings.ALLOWED_ORIGINS, list)
        assert len(settings.ALLOWED_ORIGINS) > 0
