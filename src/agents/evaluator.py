"""
Agente Evaluador: Calcula el score de riesgo combinando reglas
determinísticas, análisis de mercado, comparativo y semántico.
"""

import json
from openai import AsyncOpenAI

SCORING_RULES = {
    "brand_explicit": {"weight": 20, "category": "reglas_deterministicas"},
    "model_specific": {"weight": 20, "category": "reglas_deterministicas"},
    "no_equivalent_expression": {"weight": 15, "category": "reglas_deterministicas"},
    "restrictive_certification": {"weight": 15, "category": "reglas_deterministicas"},
    "excessive_experience": {"weight": 10, "category": "reglas_deterministicas"},
    "few_providers": {"weight": 10, "category": "analisis_mercado"},
    "market_concentration": {"weight": 10, "category": "analisis_mercado"},
    "geographic_limitation": {"weight": 5, "category": "analisis_mercado"},
    "divergence_from_similar": {"weight": 10, "category": "analisis_comparativo"},
    "more_restrictive": {"weight": 10, "category": "analisis_comparativo"},
    "brochure_similarity": {"weight": 15, "category": "analisis_semantico"},
    "product_aligned_language": {"weight": 10, "category": "analisis_semantico"},
    "weak_justification": {"weight": 10, "category": "analisis_semantico"},
}

SYSTEM_PROMPT = """Eres un evaluador de riesgos de direccionamiento en contrataciones públicas peruanas.
Recibes el análisis documental, comparativo y de mercado de un documento de contratación.

Aplica las siguientes reglas de scoring y determina cuáles indicadores están presentes:

REGLAS:
- brand_explicit (20 pts): Mención explícita de marca sin justificación
- model_specific (20 pts): Mención de modelo específico
- no_equivalent_expression (15 pts): Ausencia de "o equivalente/similar"
- restrictive_certification (15 pts): Certificación restrictiva no justificada
- excessive_experience (10 pts): Experiencia excesivamente específica
- few_providers (10 pts): Menos de 3 proveedores potenciales
- market_concentration (10 pts): Concentración de mercado aparente
- geographic_limitation (5 pts): Limitación geográfica observable
- divergence_from_similar (10 pts): Divergencia significativa vs procesos similares
- more_restrictive (10 pts): Más restrictivo que el promedio
- brochure_similarity (15 pts): Alta similitud con ficha comercial
- product_aligned_language (10 pts): Lenguaje alineado a producto específico
- weak_justification (10 pts): Justificación técnica débil

RETORNA SOLO JSON:
{
  "total_score": 0,
  "detected_indicators": [{"rule": "...", "detected": true/false, "evidence": "..."}],
  "alerts": [{
    "description": "descripción de la alerta",
    "score": 0,
    "fragment": "fragmento del documento",
    "recommendation": "recomendación",
    "indicators": [{"indicator": "...", "category": "...", "weight": 0, "evidence": "...", "source": "..."}]
  }],
  "scoring_justification": "justificación del score total"
}
"""


class EvaluatorAgent:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def evaluate(self, analysis: dict, comparison: dict, investigation: dict) -> dict:
        user_prompt = (
            f"ANÁLISIS DOCUMENTAL:\n{json.dumps(analysis, ensure_ascii=False)}\n\n"
            f"ANÁLISIS COMPARATIVO:\n{json.dumps(comparison, ensure_ascii=False)}\n\n"
            f"INVESTIGACIÓN DE MERCADO:\n{json.dumps(investigation, ensure_ascii=False)}\n\n"
            f"Evalúa el riesgo de direccionamiento aplicando las reglas de scoring."
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"total_score": 0, "detected_indicators": [], "alerts": [], "scoring_justification": "Error en evaluación."}
