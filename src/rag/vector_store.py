"""Gestión del vector store con ChromaDB."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from openai import AsyncOpenAI
from src.core.config import settings


class VectorStoreManager:
    """Wrapper sobre ChromaDB para búsqueda semántica."""

    def __init__(self):
        self.client = None
        self.collection = None
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def initialize(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    async def _get_embedding(self, text: str) -> list[float]:
        response = await self.openai.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text,
        )
        return response.data[0].embedding

    async def add(self, doc_id: str, content: str, metadata: dict = None):
        embedding = await self._get_embedding(content)
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata or {}],
        )

    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self.collection.count() == 0:
            return []
        embedding = await self._get_embedding(query)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, self.collection.count()),
        )
        docs = []
        for i in range(len(results["ids"][0])):
            docs.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
        return docs
