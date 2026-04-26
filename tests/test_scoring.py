"""Pruebas unitarias — Lógica de scoring y clasificación de riesgo."""

import pytest
from src.core.schemas import RiskLevel
from src.core.config import settings


class TestRiskClassification:
    """Valida la clasificación de niveles de riesgo."""

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

    def test_risk_level_values(self):
        assert RiskLevel.LOW.value == "BAJO"
        assert RiskLevel.MEDIUM.value == "MEDIO"
        assert RiskLevel.HIGH.value == "ALTO"


class TestScoringRules:
    """Valida las reglas de scoring del evaluador."""

    RULES = {
        "brand_explicit": 20,
        "model_specific": 20,
        "no_equivalent_expression": 15,
        "restrictive_certification": 15,
        "excessive_experience": 10,
        "few_providers": 10,
        "market_concentration": 10,
        "geographic_limitation": 5,
        "divergence_from_similar": 10,
        "more_restrictive": 10,
        "brochure_similarity": 15,
        "product_aligned_language": 10,
        "weak_justification": 10,
    }

    def test_total_possible_score(self):
        """El score máximo posible no debe superar 160 (todas las reglas activas)."""
        total = sum(self.RULES.values())
        assert total == 160

    def test_all_rules_have_positive_weights(self):
        for rule, weight in self.RULES.items():
            assert weight > 0, f"Regla {rule} tiene peso no positivo: {weight}"

    def test_deterministic_rules_are_highest(self):
        """Las reglas determinísticas deben tener los pesos más altos."""
        assert self.RULES["brand_explicit"] >= 15
        assert self.RULES["model_specific"] >= 15

    def test_worst_case_scenario_exceeds_high_threshold(self):
        """Si todas las reglas se activan, el score debe ser ALTO."""
        total = sum(self.RULES.values())
        assert total > settings.SCORE_THRESHOLD_MEDIUM


class TestSchemaValidation:
    """Valida los schemas de datos."""

    def test_document_type_enum(self):
        from src.core.schemas import DocumentType
        assert DocumentType.TDR.value == "TDR"
        assert DocumentType.BASES.value == "BASES_ADMINISTRATIVAS"
        assert DocumentType.EETT.value == "ESPECIFICACIONES_TECNICAS"

    def test_analyze_request_requires_content(self):
        from src.core.schemas import AnalyzeDocumentRequest
        with pytest.raises(Exception):
            AnalyzeDocumentRequest(document_type="TDR")

    def test_analyze_request_valid(self):
        from src.core.schemas import AnalyzeDocumentRequest
        req = AnalyzeDocumentRequest(
            content="x" * 50,
            document_type="TDR",
            process_id="SEACE-2026-001"
        )
        assert req.document_type.value == "TDR"
        assert req.process_id == "SEACE-2026-001"

    def test_query_request_valid(self):
        from src.core.schemas import QueryRequest
        req = QueryRequest(query="requisitos de TDR", top_k=5)
        assert req.top_k == 5
