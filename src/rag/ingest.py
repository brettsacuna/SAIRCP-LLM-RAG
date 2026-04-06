"""Pipeline de ingesta: chunking + embedding + almacenamiento."""

import uuid
from src.rag.vector_store import VectorStoreManager
from src.core.config import settings


class IngestPipeline:
    def __init__(self, vector_store: VectorStoreManager):
        self.vs = vector_store

    def _chunk_text(self, text: str) -> list[str]:
        """Divide texto en chunks con overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + settings.CHUNK_SIZE
            chunks.append(text[start:end])
            start += settings.CHUNK_SIZE - settings.CHUNK_OVERLAP
        return chunks

    async def ingest(self, documents: list[dict], collection: str = None) -> tuple[int, list[str]]:
        count = 0
        errors = []
        for doc in documents:
            try:
                content = doc.get("content", "")
                metadata = doc.get("metadata", {})
                chunks = self._chunk_text(content)
                for i, chunk in enumerate(chunks):
                    doc_id = f"{doc.get('id', uuid.uuid4().hex[:8])}_chunk_{i}"
                    await self.vs.add(doc_id, chunk, {**metadata, "chunk_index": i})
                    count += 1
            except Exception as e:
                errors.append(f"Error ingesting doc {doc.get('id','?')}: {str(e)}")
        return count, errors
