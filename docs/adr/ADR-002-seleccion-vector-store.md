# ADR-002: Selección del Vector Store

**Fecha:** 06/04/2026  
**Estado:** Aceptado  
**Autores:** Brett Sacuña

## Contexto

El sistema necesita un almacén de vectores para indexar documentos de contratación históricos del SEACE y permitir búsqueda semántica (RAG). Los requisitos clave son: persistencia local (compatible con despliegue on-premise del OECE), búsqueda por similitud coseno con embeddings de 1536 dimensiones (text-embedding-3-small), capacidad para ~100K documentos en fase MVP, y cero dependencia de servicios cloud externos para el almacén vectorial.

## Decisión

Se selecciona **ChromaDB** como vector store del sistema.

## Consecuencias Positivas

- Persistencia local en disco (compatible con infraestructura on-premise del OECE)
- Zero-config: no requiere servidor separado ni infraestructura adicional
- Soporte nativo de búsqueda por similitud coseno con algoritmo HNSW
- API Python nativa, integración directa sin SDK adicional
- Licencia Apache 2.0 (open-source, sin restricciones comerciales)
- Adecuado para volúmenes de hasta ~1M documentos sin degradación significativa
- Bajo consumo de recursos (~500MB RAM para 100K documentos con embeddings de 1536d)

## Consecuencias Negativas / Trade-offs

- No soporta búsqueda distribuida ni sharding nativo (limitación para escalabilidad horizontal futura)
- Menor madurez que soluciones enterprise como Pinecone o Weaviate
- Sin consola de administración web nativa (monitoreo vía código)
- Backup y recuperación requieren gestión manual del directorio de persistencia

## Alternativas Consideradas

- **Pinecone:** Managed service con excelente rendimiento y escalabilidad, pero requiere conexión cloud permanente (incompatible con requisito on-premise), pricing por volumen que escala rápidamente (~$70/mes para 1M vectores), y vendor lock-in. Descartado por incompatibilidad con despliegue on-premise.
- **Weaviate:** Self-hosted con más features (hybrid search, multi-tenancy), pero requiere más recursos (mínimo 2GB RAM), configuración compleja y overhead operativo excesivo para MVP. Candidato para fase de producción.
- **pgvector (extensión PostgreSQL):** Reutilizaría la base PostgreSQL existente, pero menor rendimiento en búsqueda ANN comparado con soluciones especializadas y requiere tuning manual de índices HNSW. Viable como alternativa futura para consolidar infraestructura.
