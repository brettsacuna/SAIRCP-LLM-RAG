"""
Agente Generador: Construye el informe final con alertas,
evidencia trazable y recomendaciones.
"""

import json
from openai import AsyncOpenAI

SYSTEM_PROMPT = """Eres un generador de informes de riesgo para contrataciones públicas peruanas.
Recibes toda la información del análisis y produces un resumen ejecutivo claro.

RETORNA SOLO JSON:
{
  "summary": "Resumen ejecutivo del análisis (máximo 500 palabras, en español)",
  "key_findings": ["hallazgo 1", "hallazgo 2"],
  "recommendations": ["recomendación 1", "recomendación 2"]
}

El resumen debe ser claro, objetivo y no concluyente (es apoyo, no decisión).
"""


class ReporterAgent:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def generate_report(
        self, analysis: dict, comparison: dict,
        investigation: dict, scoring: dict, document_type: str
    ) -> dict:
        user_prompt = (
            f"Genera el informe final para un documento tipo '{document_type}'.\n\n"
            f"SCORING: {json.dumps(scoring, ensure_ascii=False)}\n\n"
            f"ANÁLISIS: {json.dumps(analysis, ensure_ascii=False)}\n\n"
            f"COMPARACIÓN: {json.dumps(comparison, ensure_ascii=False)}\n\n"
            f"MERCADO: {json.dumps(investigation, ensure_ascii=False)}"
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"summary": "Error generando informe.", "key_findings": [], "recommendations": []}
