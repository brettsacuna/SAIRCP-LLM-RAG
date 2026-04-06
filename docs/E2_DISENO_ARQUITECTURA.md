# 🤖 Plantilla Oficial de Documentación — Proyecto Final AI/LLM

**Programa:** AI-LLM Solution Architect  
**Curso:** 5 — Proyecto Final de Arquitectura e Integración AI/LLM  
**Documento:** Entregable 2 — Diseño de Arquitectura (Cap. 2)

---

## 📋 Información General del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre del Proyecto** | SAIRCP-LLM-RAG: Sistema de Apoyo para Identificación de Riesgos en Contrataciones Públicas mediante IA |
| **Participante(s)** | Brett Sacuña |
| **Instructor** | *[Nombre del instructor]* |
| **Cohorte / Edición** | Cohorte 2025-A |
| **Fecha de Inicio** | 06/04/2026 |
| **Fecha de Entrega Final** | *[DD/MM/AAAA]* |
| **Versión del Documento** | v1.0 |
| **Estado del Proyecto** | En Desarrollo |
| **Repositorio GitHub/GitLab** | https://github.com/brettsacuna/SAIRCP-LLM-RAG |
| **Entorno Cloud** | Hybrid (on-premise + OpenAI API) |
| **Stack Tecnológico Principal** | Python 3.11, FastAPI, OpenAI GPT-4o, ChromaDB, PostgreSQL 16, Docker |

---

## 3. Diseño de Arquitectura AI/LLM

### 3.1 Diagrama de Arquitectura General (Nivel C4 — Contexto y Contenedor)

> Los diagramas C4 de Contexto y Contenedor se encuentran como archivos SVG de alta resolución en `/docs/architecture/`. A continuación se describe cada nivel.

**Nivel Contexto:** El sistema SAIRCP se posiciona como un módulo integrado al ecosistema del SEACE 4.0. Interactúa con tres tipos de actores (usuarios operativos del SEACE, Dirección del SEACE como gobernanza funcional, e instancias de supervisión/control) y con cuatro sistemas externos (SEACE 4.0 para procesos históricos, Registro Nacional de Proveedores para validación de mercado, fuentes web abiertas nacionales, y OpenAI API como proveedor de inferencia LLM).

**Nivel Contenedor:** La arquitectura interna se descompone en:
- **Capa de Presentación:** Frontend Angular integrado al SEACE + API Gateway FastAPI
- **Capa de Orquestación:** Backend del módulo IA con orquestador de 5 agentes especializados
- **Capa de Procesamiento:** Motor documental (extracción PDF/DOCX), Motor IA (RAG + LLM), Motor de scoring (reglas + pesos)
- **Capa de Datos:** ChromaDB (vector store), PostgreSQL (auditoría/metadata), OpenSearch (indexación documental)

*Figura 1. Diagrama C4 Contexto — ver `/docs/architecture/saircp_c4_context_diagram`*  
*Figura 2. Diagrama C4 Contenedor — ver `/docs/architecture/saircp_c4_container_diagram`*

### 3.2 Descripción de Componentes Arquitectónicos

| Componente | Tecnología / Servicio | Responsabilidad Principal | Justificación de Selección |
|------------|----------------------|--------------------------|---------------------------|
| API Gateway | FastAPI 0.115+ | Enrutamiento REST, validación de schemas, rate limiting, health check | Framework Python nativo async con auto-generación de OpenAPI/Swagger, alto rendimiento con Uvicorn, curva de aprendizaje baja para el equipo |
| Orquestador LLM | Implementación custom (AgentOrchestrator) | Coordinación secuencial de 5 agentes especializados, manejo de contexto entre agentes | Evita dependencia de LangChain (over-engineering para este caso); control total del flujo, debugging directo, sin abstracciones innecesarias (ver ADR-003) |
| Modelo LLM Base | OpenAI GPT-4o | Análisis semántico, extracción estructurada, evaluación de riesgo, generación de informes | JSON mode nativo, excelente comprensión de español legal/administrativo, 128K context window, latencia competitiva (ver ADR-001) |
| Embeddings | OpenAI text-embedding-3-small | Vectorización de documentos para búsqueda semántica RAG | 1536 dimensiones, costo 5x menor que text-embedding-3-large, rendimiento adecuado para español, integración directa con la API ya utilizada |
| Vector Store | ChromaDB 0.5+ | Almacenamiento y búsqueda de similitud coseno para RAG | Persistencia local (compatible on-premise OECE), zero-config, HNSW nativo, Apache 2.0, bajo consumo de recursos (ver ADR-002) |
| Base de Datos | PostgreSQL 16 | Persistencia de auditoría, bitácoras, metadata de análisis, usuarios | Motor maduro, robusto, ya presente en la infraestructura institucional del OECE |
| Motor de Búsqueda | OpenSearch | Indexación full-text de documentos SEACE, búsqueda por términos y filtros | Fork open-source de Elasticsearch, compatible con la infraestructura institucional, soporte de búsqueda en español |
| Observabilidad | structlog + logging estándar Python | Logs estructurados JSON, trazabilidad de cada análisis | Integrable con cualquier stack de monitoreo futuro (ELK, Grafana Loki), sin vendor lock-in |
| Seguridad / IAM | JWT (python-jose) + OAuth 2.0 integrado a SEACE | Autenticación/autorización mediante sesión institucional existente | Reutiliza el mecanismo de identidad del SEACE 4.0, sin crear un segundo sistema de login |
| Contenedores | Docker + Docker Compose | Empaquetamiento, despliegue reproducible, aislamiento de servicios | Estándar de la industria, compatible con OpenShift institucional, facilita CI/CD |

### 3.3 Diagrama de Flujo de Datos e Integración

El ciclo completo de una solicitud de análisis sigue 7 pasos secuenciales:

1. **Carga de documento:** El usuario sube un PDF/DOCX o el sistema lee el documento asociado al proceso SEACE.
2. **Extracción de texto:** PyMuPDF (PDF) o python-docx (DOCX) extraen el contenido textual limpio.
3. **Agente Analizador:** GPT-4o con JSON mode extrae requisitos técnicos, comerciales, documentales, marcas mencionadas, certificaciones, y evalúa la calidad de la justificación técnica.
4. **Agente Comparador + Investigador (parallelizable en fase 2):**
   - Comparador: Busca en ChromaDB procesos similares vía embeddings y detecta divergencias.
   - Investigador: Consulta fuentes externas (RNP, web abierta) para evaluar pluralidad de proveedores.
5. **Agente Evaluador:** Aplica el modelo de scoring híbrido (13 indicadores con pesos, total 0-100) y genera alertas con evidencia.
6. **Agente Generador:** Construye el informe final con resumen ejecutivo, hallazgos clave y recomendaciones.
7. **Respuesta al usuario:** Se retorna el score de riesgo (BAJO/MEDIO/ALTO), las alertas con fragmentos del documento resaltados, y la evidencia trazable. Se registra la bitácora de auditoría.

*Figura 3. Flujo de datos request→response — ver `/docs/architecture/saircp_data_flow_request_response`*

### 3.4 Estrategia de Diseño de Prompts y RAG

**System Prompt Base (Agente Analizador):**

```
Eres un analista experto en contrataciones públicas del Perú (Ley 30225 y su Reglamento).
Tu tarea es analizar documentos de contratación (TDR, bases administrativas, especificaciones
técnicas, estudios de mercado) y extraer información estructurada.

DEBES RETORNAR SOLO JSON VÁLIDO con esta estructura exacta:
{
  "requirements": ["lista de requisitos técnicos, comerciales y documentales"],
  "restrictions": ["posibles restricciones a la competencia detectadas"],
  "brands_mentioned": ["marcas o modelos específicos"],
  "certifications": ["certificaciones exigidas"],
  "experience_requirements": ["requisitos de experiencia"],
  "geographic_restrictions": ["restricciones geográficas"],
  "equivalent_expression_present": true/false,
  "technical_justification_quality": "fuerte|débil|ausente",
  "key_fragments": [{"text": "fragmento", "reason": "relevancia"}]
}

RESTRICCIONES:
- Analiza SOLO en base al contenido proporcionado.
- No inventes información que no esté en el documento.
- Sé preciso en la extracción de fragmentos textuales.
- Identifica lenguaje alineado a fichas comerciales específicas.

FORMATO DE RESPUESTA: JSON estricto según el schema indicado.
```

Cada agente tiene su propio system prompt especializado con instrucciones, restricciones y schema de salida JSON específico. Los 5 prompts completos se encuentran documentados en el código fuente (`src/agents/*.py`).

**Parámetros del modelo:**
- `temperature: 0.0` (determinismo para reproducibilidad)
- `response_format: {"type": "json_object"}` (garantía de JSON válido)
- `max_tokens: 4096` (suficiente para respuestas estructuradas)
- Seed fijo para consistencia entre ejecuciones (pendiente implementación)

### 3.5 Arquitectura Física (Equivalencias por Nube)

| Capa | AWS | GCP | On-Premise (OECE) |
|---|---|---|---|
| Ingesta | Lambda / ECS | Cloud Run | Docker container |
| Almacenamiento documentos | S3 | GCS | Filesystem / MinIO |
| Vector Store | OpenSearch Serverless | Vertex AI Vector Search | ChromaDB (local) |
| Base de datos | RDS PostgreSQL | Cloud SQL | PostgreSQL 16 |
| Orquestación | ECS / EKS | Cloud Run / GKE | Docker Compose / OpenShift |
| Observabilidad | CloudWatch | Cloud Monitoring | structlog + Grafana |
| LLM Provider | OpenAI API (externo) | OpenAI API (externo) | OpenAI API (externo) |

**Estrategia de Recuperación (RAG):**

| Parámetro | Valor | Justificación |
|---|---|---|
| **Tipo de chunking** | Recursivo por caracteres | Preserva integridad de párrafos y secciones legales |
| **Chunk size** | 1000 caracteres | Balance entre contexto suficiente y precisión de retrieval; documentos de contratación tienen párrafos de ~300-800 caracteres |
| **Chunk overlap** | 200 caracteres (20%) | Evita cortes en medio de requisitos técnicos que abarcan múltiples oraciones |
| **Modelo de embeddings** | text-embedding-3-small (1536d) | Costo-efectivo ($0.02/1M tokens), rendimiento sólido en español, misma API de OpenAI |
| **Función de similitud** | Coseno (HNSW en ChromaDB) | Estándar para embeddings normalizados, eficiente en alta dimensionalidad |
| **Top-K** | 5 documentos | Balanceo entre contexto relevante y consumo de tokens; 5 chunks × 1000 chars ≈ 1250 tokens de contexto |
| **Similarity threshold** | 0.75 | Filtra chunks irrelevantes; calibrado empíricamente con documentos de prueba SEACE |
| **Re-ranking** | No implementado en MVP | Candidato para fase 2 con Cohere Rerank o cross-encoder |

---

## 4. Diseño de APIs y Conectores

### 4.1 Especificación de Endpoints (API REST)

La especificación completa OpenAPI 3.1 se encuentra en `/docs/api/openapi.yaml`. Endpoints principales:

| Endpoint | Método | Descripción | Request Body / Params | Response Schema |
|----------|--------|-------------|----------------------|-----------------|
| `/api/v1/health` | `GET` | Health check del sistema y componentes | N/A | `{"status": "healthy\|degraded", "version": string, "components": object, "timestamp": datetime}` |
| `/api/v1/analyze` | `POST` | Analiza documento de contratación (texto) | `{"content": string (min 50 chars), "document_type": enum, "process_id?": string, "entity_name?": string}` | `AnalysisResult` con score, alertas, evidencia, proveedores |
| `/api/v1/analyze/upload` | `POST` | Analiza documento cargado (PDF/DOCX) | `multipart/form-data: file` | `AnalysisResult` (mismo schema) |
| `/api/v1/ingest` | `POST` | Ingesta documentos al vector store | `{"documents": [{content, metadata}], "collection?": string}` | `{"status": string, "indexed_docs": int, "errors": []}` |
| `/api/v1/query` | `POST` | Consulta RAG en lenguaje natural | `{"query": string (min 5 chars), "session_id?": string, "top_k?": int (1-20)}` | `{"response": string, "sources": [], "tokens_used": int, "latency_ms": float}` |

**Schema principal — AnalysisResult:**

```json
{
  "analysis_id": "ANA-a1b2c3d4e5f6",
  "timestamp": "2026-04-06T15:30:00Z",
  "document_type": "TDR",
  "total_score": 65,
  "risk_level": "ALTO",
  "alerts": [
    {
      "alert_id": "ALT-a1b2c3d4e5f6-001",
      "description": "Mención explícita de marca sin expresión equivalente",
      "severity": "ALTO",
      "indicators": [
        {
          "indicator": "brand_explicit",
          "category": "reglas_deterministicas",
          "weight": 20,
          "evidence": "Se requiere servidor Dell PowerEdge R750",
          "source": "regla"
        }
      ],
      "document_fragment": "...se requiere servidor Dell PowerEdge R750 con procesador Intel Xeon...",
      "recommendation": "Incluir la expresión 'o equivalente' y justificar técnicamente la marca si aplica"
    }
  ],
  "summary": "El documento presenta un nivel de riesgo ALTO (score 65/100)...",
  "requirements_found": ["Servidor rack 2U", "Certificación ISO 27001", "..."],
  "potential_restrictions": ["Marca específica sin equivalente", "..."],
  "comparable_processes": [{"id": "SEACE-2025-001234", "similarity_score": 0.87}],
  "providers_found": [{"name": "Empresa X", "ruc": "20123456789", "source": "RNP"}],
  "processing_time_ms": 12450.5,
  "model_used": "gpt-4o",
  "trace_id": "uuid-trace-completo"
}
```

### 4.2 Autenticación y Autorización

| Campo | Descripción |
|-------|-------------|
| **Mecanismo Auth** | JWT Bearer Token integrado con sesión del SEACE 4.0 (OAuth 2.0) |
| **Proveedor de Identidad** | Sistema de autenticación institucional del SEACE (SSO existente) |
| **Gestión de Secrets** | Variables de entorno en contenedor + `.env` (desarrollo); en producción: secrets manager institucional |
| **Rate Limiting** | 10 análisis/min por usuario, 100 análisis/min global (ajustable) |
| **Roles definidos** | `analista` (ejecutar análisis, ver resultados), `supervisor` (ver auditoría, configurar reglas), `admin` (gestión completa) |

**Matriz RBAC:**

| Acción | analista | supervisor | admin |
|--------|----------|-----------|-------|
| Ejecutar análisis | ✅ | ✅ | ✅ |
| Ver resultados propios | ✅ | ✅ | ✅ |
| Ver auditoría global | ❌ | ✅ | ✅ |
| Configurar reglas scoring | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Ingestar documentos | ❌ | ❌ | ✅ |

### 4.3 Conectores de Fuentes de Datos

| Fuente de Datos | Tipo | Conector/SDK | Frecuencia de Sync | Manejo de Errores |
|----------------|------|-------------|-------------------|------------------|
| SEACE 4.0 — Procesos históricos | API REST institucional | httpx AsyncClient | Batch diario (ingesta al vector store) | Retry x3 con backoff exponencial, cache local de 24h |
| RNP — Registro Nacional de Proveedores | API REST OSCE | httpx AsyncClient | Consulta en tiempo real por análisis | Timeout 10s, respuesta parcial si no disponible, log de fallo |
| Fuentes web abiertas nacionales | Web scraping / APIs públicas | httpx + BeautifulSoup | Consulta en tiempo real por análisis | Timeout 15s, resultado "no disponible" si falla, sin bloqueo del flujo |
| OpenAI API | API REST (LLM + Embeddings) | openai SDK Python | Tiempo real por cada agente | Retry x3 con backoff, fallback a GPT-4o-mini si error persistente |
| ChromaDB (Vector Store) | Base vectorial local | chromadb Python client | Persistencia continua (disco local) | Auto-recovery, backup diario del directorio de datos |
| PostgreSQL (Auditoría) | Base relacional | asyncpg / SQLAlchemy | Escritura en tiempo real | Connection pool (5-20), retry automático, dead-letter log si falla |

---

## 5. Seguridad, Cumplimiento y Ética

### 5.1 Modelo de Amenazas y Controles de Seguridad

| Amenaza / Riesgo | Vector de Ataque | Nivel | Control Implementado | Justificación Técnica |
|-----------------|-----------------|-------|---------------------|----------------------|
| Prompt Injection | Input malicioso en el campo de contenido del documento | **ALTO** | Validación de input (longitud, caracteres), system prompts con instrucciones estrictas de formato JSON, temperatura 0.0 | Los system prompts delimitan estrictamente el comportamiento del LLM; JSON mode impide respuestas de formato libre |
| Data Leakage | Documento con PII enviado a OpenAI | **ALTO** | Política de zero-retention de OpenAI API (Tier 2+), no se almacenan prompts fuera del perímetro, disclaimers institucionales | OpenAI API no usa datos de API para entrenamiento; se recomienda evaluación de modelo on-premise para fase 2 |
| API Key Exposure | OPENAI_API_KEY en repositorio o logs | **CRÍTICO** | `.env` excluido de Git (`.gitignore`), variables de entorno en contenedor, rotación periódica de keys | Separación de configuración y código; en producción usar secrets manager institucional |
| DoS / Abuso de API | Volumen excesivo de análisis por un usuario | **MEDIO** | Rate limiting (10 análisis/min por usuario), validación de sesión JWT, límite de tamaño de archivo (20MB) | FastAPI middleware + validación en capa de API Gateway |
| Falsificación de resultados | Manipulación del score o alertas en tránsito | **MEDIO** | HTTPS obligatorio, JWT firmado, bitácora de auditoría inmutable con hash del resultado | Trazabilidad completa: cada análisis queda registrado con trace_id |
| Alucinación del LLM | El modelo genera riesgos inexistentes (falsos positivos) | **ALTO** | Modelo híbrido: reglas determinísticas + LLM; validación cruzada entre agentes; evidencia con fragmentos textuales reales | Las alertas siempre incluyen el fragmento exacto del documento; el score combina reglas verificables con análisis semántico |

### 5.2 Cumplimiento Regulatorio

| Regulación | Requerimiento Aplicable | Control Implementado | Evidencia |
|-----------|------------------------|---------------------|-----------|
| Ley 29733 (Protección de Datos Personales — Perú) | Los documentos pueden contener datos de personas naturales (proveedores, firmantes) | No se almacenan datos personales fuera del perímetro institucional; logs anonimizados; OpenAI zero-retention | Configuración de la API, política de retención |
| D.U. 007-2020 (Marco de Confianza Digital) | Interoperabilidad y seguridad en servicios digitales del Estado | APIs REST con estándares abiertos (OpenAPI 3.1), autenticación OAuth 2.0, logs estructurados | Especificación OpenAPI, configuración de seguridad |
| Ley 30225 (Contrataciones del Estado) | El sistema no debe sustituir la evaluación humana ni constituir prueba de ilegalidad | Disclaimer explícito en cada informe: "Este resultado es de apoyo y no constituye determinación de ilegalidad"; carácter no decisorio | Texto del disclaimer en el Agente Generador |
| Lineamientos OECE | Trazabilidad y gobernanza del sistema | Bitácora de auditoría 100% de los análisis (usuario, fecha, documento, resultado, trace_id) | Tabla de auditoría en PostgreSQL |

### 5.3 Marco Ético de la Solución AI

| Dimensión Ética | Riesgo Identificado | Mecanismo de Mitigación |
|----------------|--------------------|-----------------------|
| Sesgos algorítmicos | El modelo puede priorizar patrones de ciertos sectores/industrias sobre otros debido a distribución desigual de datos de entrenamiento | Evaluación periódica de distribución de alertas por sector; dataset de validación balanceado; auditoría del modelo con expertos en contrataciones |
| Transparencia y explicabilidad | Los usuarios deben comprender por qué se generó cada alerta | Cada alerta incluye: fragmento del documento, regla aplicada, peso del indicador, fuente consultada; score desglosado por categoría |
| Alucinaciones | GPT-4o puede generar riesgos ficticios con apariencia convincente | Modelo híbrido (reglas verificables + LLM); evidencia obligatoria con texto real del documento; temperature=0.0 para máximo determinismo |
| Uso indebido de resultados | El informe podría interpretarse como prueba concluyente de corrupción | Disclaimer legal en cada informe; capacitación a usuarios; el sistema se denomina explícitamente "de apoyo"; sin capacidad de bloqueo de procesos |
| Privacidad de datos | Documentos de contratación contienen información sensible | OpenAI API zero-retention policy; no se almacenan prompts ni respuestas fuera de la infraestructura institucional; anonimización de logs |

---

## Anexo A — Architecture Decision Records (ADR)

Los ADRs completos se encuentran en `/docs/adr/`. Resumen:

### ADR-001: Selección del Modelo LLM Base

**Decisión:** OpenAI GPT-4o  
**Alternativas descartadas:** Claude 3.5 Sonnet (menor ecosistema LATAM), Gemini 1.5 Pro (menor consistencia JSON), Llama 3.1 70B (requiere GPU, incompatible con cronograma MVP), GPT-4o-mini (menor razonamiento)  
**Justificación clave:** JSON mode nativo, excelente español legal, 128K context, latencia competitiva.

### ADR-002: Selección del Vector Store

**Decisión:** ChromaDB  
**Alternativas descartadas:** Pinecone (requiere cloud, incompatible on-premise), Weaviate (overhead excesivo para MVP), pgvector (menor rendimiento ANN)  
**Justificación clave:** Persistencia local, zero-config, HNSW nativo, Apache 2.0.

### ADR-003: Arquitectura Multi-Agente Secuencial

**Decisión:** 5 agentes especializados orquestados secuencialmente  
**Alternativas descartadas:** Prompt monolítico (no debuggeable, sin trazabilidad), LangChain LCEL (over-engineering), agentes paralelos (complejidad prematura)  
**Justificación clave:** Explicabilidad por paso, testabilidad unitaria, extensibilidad.

---

## Referencias

1. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS 2020*, vol. 33, pp. 9459–9474.
2. OpenAI, "GPT-4 Technical Report," arXiv:2303.08774, 2023.
3. OpenAI, "Text Embeddings Documentation," [Online]. Available: https://platform.openai.com/docs/guides/embeddings
4. ChromaDB, "ChromaDB Documentation," [Online]. Available: https://docs.trychroma.com
5. FastAPI, "FastAPI Documentation," [Online]. Available: https://fastapi.tiangolo.com
6. OSCE Perú, "Ley 30225 — Ley de Contrataciones del Estado," [Online]. Available: https://www.gob.pe/osce
7. M. Kleppmann, *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
8. B. Beyer et al., *Site Reliability Engineering*. O'Reilly Media, 2016.
9. LangChain, "LangChain Documentation v0.2," [Online]. Available: https://python.langchain.com/docs
10. OWASP, "OWASP Top 10 for LLM Applications," 2025. [Online]. Available: https://owasp.org/www-project-top-10-for-large-language-model-applications/
