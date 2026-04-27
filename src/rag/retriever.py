"""Retriever: consulta RAG con generación aumentada."""

from openai import AsyncOpenAI

from src.core.config import settings
from src.rag.vector_store import VectorStoreManager

RAG_SYSTEM_PROMPT = """Eres un asistente experto en contrataciones públicas del Perú (OECE/SEACE).
Responde SOLO en base al contexto proporcionado. Si no tienes información suficiente,
indica "No tengo información sobre eso en la base de conocimiento."
Responde siempre en español con tono técnico-institucional."""


class RAGRetriever:
    def __init__(self, vector_store: VectorStoreManager):
        self.vs = vector_store
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def query(self, query: str, top_k: int = 5) -> tuple[str, list[dict], int]:
        docs = await self.vs.search(query, top_k=top_k)
        context = "\n\n".join([f"[Fuente: {d['id']}]\n{d['content']}" for d in docs])
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL, temperature=0.0,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": f"CONTEXTO:\n{context}\n\nPREGUNTA: {query}"},
            ],
        )
        tokens = response.usage.total_tokens if response.usage else 0
        sources = [{"id": d["id"], "distance": d.get("distance")} for d in docs]
        return response.choices[0].message.content, sources, tokens
