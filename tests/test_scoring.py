"""Pruebas unitarias — Lógica de scoring, schemas y clasificación de riesgo."""

import pytest

from src.core.schemas import RiskLevel, DocumentType, AnalyzeDocumentRequest, QueryRequest, IngestDocumentRequest
from src.core.config import settings


class TestRiskClassification:
    def _classify(self, score: int) -> RiskLevel:
        if score <= settings.SCORE_THRESHOLD_LOW:
            return RiskLevel.LOW
        elif score <= settings.SCORE_THRESHOLD_MEDIUM:
            return RiskLevel.MEDIUM
        return RiskLevel.HIGH

    def test_score_zero_is_low(self):
        assert self._classify(0) == RiskLevel.LOW

    def test_score_at_low_boundary(self):
        assert self._classify(30) == RiskLevel.LOW

    def test_score_just_above_low(self):
        assert self._classify(31) == RiskLevel.MEDIUM

    def test_score_at_medium_boundary(self):
        assert self._classify(60) == RiskLevel.MEDIUM

    def test_score_just_above_medium(self):
        assert self._classify(61) == RiskLevel.HIGH

    def test_score_max(self):
        assert self._classify(100) == RiskLevel.HIGH

    def test_negative_score_is_low(self):
        assert self._classify(-5) == RiskLevel.LOW

    def test_risk_level_values(self):
        assert RiskLevel.LOW.value == "BAJO"
        assert RiskLevel.MEDIUM.value == "MEDIO"
        assert RiskLevel.HIGH.value == "ALTO"

    def test_risk_level_is_string(self):
        assert isinstance(RiskLevel.LOW, str)


class TestScoringRules:
    RULES = {
        "brand_explicit": 20, "model_specific": 20,
        "no_equivalent_expression": 15, "restrictive_certification": 15,
        "excessive_experience": 10, "few_providers": 10,
        "market_concentration": 10, "geographic_limitation": 5,
        "divergence_from_similar": 10, "more_restrictive": 10,
        "brochure_similarity": 15, "product_aligned_language": 10,
        "weak_justification": 10,
    }

    def test_total_possible_score(self):
        assert sum(self.RULES.values()) == 160

    def test_rule_count(self):
        assert len(self.RULES) == 13

    def test_all_rules_have_positive_weights(self):
        for rule, weight in self.RULES.items():
            assert weight > 0, f"Regla {rule} tiene peso no positivo"

    def test_deterministic_rules_are_highest(self):
        assert self.RULES["brand_explicit"] >= 15
        assert self.RULES["model_specific"] >= 15

    def test_worst_case_exceeds_high_threshold(self):
        assert sum(self.RULES.values()) > settings.SCORE_THRESHOLD_MEDIUM

    def test_categories_exist(self):
        categories = {"reglas_deterministicas", "analisis_mercado", "analisis_comparativo", "analisis_semantico"}
        from src.agents.evaluator import SCORING_RULES
        actual = {v["category"] for v in SCORING_RULES.values()}
        assert actual == categories


class TestSchemaValidation:
    def test_document_type_enum(self):
        assert DocumentType.TDR.value == "TDR"
        assert DocumentType.BASES.value == "BASES_ADMINISTRATIVAS"
        assert DocumentType.EETT.value == "ESPECIFICACIONES_TECNICAS"
        assert DocumentType.ESTUDIO_MERCADO.value == "ESTUDIO_MERCADO"

    def test_analyze_request_requires_content(self):
        with pytest.raises(Exception):
            AnalyzeDocumentRequest(document_type="TDR")

    def test_analyze_request_valid(self):
        req = AnalyzeDocumentRequest(content="x" * 50, document_type="TDR", process_id="SEACE-2026-001")
        assert req.document_type == DocumentType.TDR
        assert req.process_id == "SEACE-2026-001"
        assert req.entity_name is None

    def test_analyze_request_with_all_fields(self):
        req = AnalyzeDocumentRequest(
            content="x" * 50, document_type="TDR",
            process_id="SEACE-2026-001", entity_name="Municipalidad"
        )
        assert req.entity_name == "Municipalidad"

    def test_query_request_valid(self):
        req = QueryRequest(query="requisitos de TDR", top_k=5)
        assert req.top_k == 5
        assert req.session_id is None

    def test_query_request_default_top_k(self):
        req = QueryRequest(query="pregunta de prueba")
        assert req.top_k == 5

    def test_ingest_request_valid(self):
        req = IngestDocumentRequest(documents=[{"content": "test"}])
        assert len(req.documents) == 1
        assert req.collection is None

    def test_ingest_request_with_collection(self):
        req = IngestDocumentRequest(documents=[{"content": "test"}], collection="custom")
        assert req.collection == "custom"
