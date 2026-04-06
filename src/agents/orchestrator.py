"""
Orquestador de agentes para análisis de documentos de contratación.
Coordina los 5 agentes especializados en secuencia.
"""

import uuid
import json
from datetime import datetime, timezone
from typing import Optional

from openai import AsyncOpenAI

from src.core.config import settings
from src.core.schemas import (
    AnalysisResult, AlertDetail, RiskIndicator, RiskLevel, DocumentType
)
from src.agents.analyzer import AnalyzerAgent
from src.agents.comparator import ComparatorAgent
from src.agents.investigator import InvestigatorAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.reporter import ReporterAgent


class AgentOrchestrator:
    """Orquesta el flujo de análisis multi-agente."""

    def __init__(self, vector_store=None):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_store = vector_store
        self.model = settings.OPENAI_MODEL

        # Inicializar agentes
        self.analyzer = AnalyzerAgent(self.client, self.model)
        self.comparator = ComparatorAgent(self.client, self.model, self.vector_store)
        self.investigator = InvestigatorAgent(self.client, self.model)
        self.evaluator = EvaluatorAgent(self.client, self.model)
        self.reporter = ReporterAgent(self.client, self.model)

    async def analyze(
        self,
        content: str,
        document_type: str,
        process_id: Optional[str] = None,
        entity_name: Optional[str] = None,
    ) -> AnalysisResult:
        """
        Pipeline completo de análisis:
        1. Analyzer  -> Extrae requisitos y restricciones
        2. Comparator -> Compara con procesos similares (RAG)
        3. Investigator -> Consulta fuentes externas (RNP, web)
        4. Evaluator  -> Calcula scoring de riesgo
        5. Reporter   -> Genera informe final con evidencia
        """
        analysis_id = str(uuid.uuid4())[:12]
        trace_id = str(uuid.uuid4())

        # --- Paso 1: Análisis documental ---
        analysis_data = await self.analyzer.extract(content, document_type)

        # --- Paso 2: Comparación con procesos similares ---
        comparison_data = await self.comparator.compare(
            requirements=analysis_data.get("requirements", []),
            document_type=document_type,
        )

        # --- Paso 3: Investigación de mercado ---
        investigation_data = await self.investigator.investigate(
            requirements=analysis_data.get("requirements", []),
            brands=analysis_data.get("brands_mentioned", []),
        )

        # --- Paso 4: Evaluación y scoring ---
        scoring_result = await self.evaluator.evaluate(
            analysis=analysis_data,
            comparison=comparison_data,
            investigation=investigation_data,
        )

        # --- Paso 5: Generación de informe ---
        report = await self.reporter.generate_report(
            analysis=analysis_data,
            comparison=comparison_data,
            investigation=investigation_data,
            scoring=scoring_result,
            document_type=document_type,
        )

        # Construir resultado final
        total_score = scoring_result.get("total_score", 0)
        risk_level = self._classify_risk(total_score)

        alerts = []
        for alert_data in scoring_result.get("alerts", []):
            indicators = [
                RiskIndicator(
                    indicator=ind.get("indicator", ""),
                    category=ind.get("category", ""),
                    weight=ind.get("weight", 0),
                    evidence=ind.get("evidence", ""),
                    source=ind.get("source", "regla"),
                )
                for ind in alert_data.get("indicators", [])
            ]
            alerts.append(AlertDetail(
                alert_id=f"ALT-{analysis_id}-{len(alerts)+1:03d}",
                description=alert_data.get("description", ""),
                severity=self._classify_risk(alert_data.get("score", 0)),
                indicators=indicators,
                document_fragment=alert_data.get("fragment", ""),
                recommendation=alert_data.get("recommendation", ""),
            ))

        return AnalysisResult(
            analysis_id=f"ANA-{analysis_id}",
            timestamp=datetime.now(timezone.utc),
            document_type=document_type,
            total_score=total_score,
            risk_level=risk_level,
            alerts=alerts,
            summary=report.get("summary", ""),
            requirements_found=analysis_data.get("requirements", []),
            potential_restrictions=analysis_data.get("restrictions", []),
            comparable_processes=comparison_data.get("similar_processes", []),
            providers_found=investigation_data.get("providers", []),
            processing_time_ms=0,  # Se setea en el endpoint
            model_used=self.model,
            trace_id=trace_id,
        )

    def _classify_risk(self, score: int) -> RiskLevel:
        if score <= settings.SCORE_THRESHOLD_LOW:
            return RiskLevel.LOW
        elif score <= settings.SCORE_THRESHOLD_MEDIUM:
            return RiskLevel.MEDIUM
        return RiskLevel.HIGH
