"""
Agente Investigador: Consulta fuentes externas (RNP, web abierta)
para validar disponibilidad de proveedores y bienes/servicios.
"""

import json
from openai import AsyncOpenAI

SYSTEM_PROMPT = """Eres un investigador de mercado especializado en contrataciones públicas peruanas.
Recibes requisitos y marcas/productos mencionados en un documento de contratación.
Tu tarea es evaluar la disponibilidad del mercado y pluralidad de proveedores.

NOTA: En esta versión MVP, simulas la consulta a fuentes externas basándote en tu conocimiento.
En producción, este agente se integrará con APIs del RNP y web scraping.

RETORNA SOLO JSON:
{
  "providers": [{"name": "...", "ruc": "...", "source": "RNP|web", "relevance": "alta|media|baja"}],
  "market_concentration": "alta|media|baja",
  "alternative_products_available": true/false,
  "market_analysis_summary": "resumen del análisis de mercado"
}
"""


class InvestigatorAgent:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def investigate(self, requirements: list, brands: list) -> dict:
        user_prompt = (
            f"Requisitos identificados:\n{json.dumps(requirements, ensure_ascii=False)}\n\n"
            f"Marcas/modelos mencionados:\n{json.dumps(brands, ensure_ascii=False)}\n\n"
            f"Evalúa la disponibilidad del mercado y pluralidad de proveedores "
            f"en el contexto peruano."
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
            return {
                "providers": [],
                "market_concentration": "desconocida",
                "alternative_products_available": False,
                "market_analysis_summary": "No se pudo completar la investigación.",
            }
