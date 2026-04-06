"""
Agente Comparador: Contrasta el documento con procesos similares
almacenados en el vector store (SEACE histórico).
"""

import json
from openai import AsyncOpenAI

SYSTEM_PROMPT = """Eres un analista comparativo de procesos de contratación pública peruana.
Recibes los requisitos extraídos de un documento y contexto de procesos similares anteriores.
Tu tarea es identificar divergencias significativas.

RETORNA SOLO JSON:
{
  "similar_processes": [{"id": "...", "description": "...", "similarity_score": 0.0}],
  "divergences": [{"requirement": "...", "comparison": "...", "severity": "alta|media|baja"}],
  "more_restrictive_than_average": true/false,
  "analysis_summary": "resumen del análisis comparativo"
}
"""


class ComparatorAgent:
    def __init__(self, client: AsyncOpenAI, model: str, vector_store=None):
        self.client = client
        self.model = model
        self.vector_store = vector_store

    async def compare(self, requirements: list, document_type: str) -> dict:
        """Compara requisitos contra procesos similares del vector store."""
        # Recuperar documentos similares del vector store
        context_docs = []
        if self.vector_store:
            query = " ".join(requirements[:5]) if requirements else document_type
            context_docs = await self.vector_store.search(query, top_k=5)

        context_text = "\n\n".join(
            [f"[Proceso: {d.get('id','N/A')}] {d.get('content','')}" for d in context_docs]
        ) if context_docs else "No se encontraron procesos comparables en la base de datos."

        user_prompt = (
            f"Requisitos del documento actual:\n"
            f"{json.dumps(requirements, ensure_ascii=False)}\n\n"
            f"Procesos similares encontrados:\n{context_text}\n\n"
            f"Realiza el análisis comparativo."
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
                "similar_processes": [],
                "divergences": [],
                "more_restrictive_than_average": False,
                "analysis_summary": "No se pudo completar el análisis comparativo.",
            }
