# SAIRCP-LLM-RAG

**Sistema de Apoyo para la Identificación de Riesgos en Contrataciones Públicas mediante IA**  
Extensión del SEACE 4.0 — OECE

[![Pipeline](https://gitlab.com/ia/saircp-llm-rag/badges/main/pipeline.svg)](https://gitlab.com/ia/saircp-llm-rag/-/pipelines)
[![Coverage](https://gitlab.com/ia/saircp-llm-rag/badges/main/coverage.svg)](https://gitlab.com/ia/saircp-llm-rag/-/pipelines)

> **URL del sistema:** https://saircp.oece.gob.pe  
> **Swagger UI:** https://saircp.oece.gob.pe/docs  
> **Video demo:** https://youtu.be/XXXXXXXXX

---

## Problema que resuelve

El direccionamiento en contrataciones públicas ocurre cuando los documentos de contratación (TDR, bases, especificaciones técnicas) se redactan con requisitos que favorecen a un proveedor específico, limitando la libre competencia. El SAIRCP analiza estos documentos usando IA para detectar indicadores de riesgo como mención de marcas sin "o equivalente", requisitos excesivos de experiencia, y lenguaje alineado a fichas comerciales.

## Stack Tecnológico

| Componente | Tecnología | Justificación |
|---|---|---|
| Backend | Python 3.11 + FastAPI | Async nativo, OpenAPI automático |
| LLM | OpenAI GPT-4o | JSON mode, español legal, 128K context |
| Embeddings | text-embedding-3-small | 1536d, costo-efectivo |
| Vector Store | ChromaDB | Persistencia local, HNSW coseno |
| Base de Datos | PostgreSQL 16 | Auditoría y metadata |
| CI/CD | GitLab CI + GitHub Actions | Pipeline 5 stages |
| Frontend | HTML/CSS/JS + Nginx | Estilo institucional OECE |
| Contenedores | Docker multi-stage + Compose | 3 servicios con health checks |

## Resultados Reales

### Métricas RAGAS (evaluación LLM)

| Métrica | Score | Umbral |
|---|---|---|
| Faithfulness | 0.85 | ≥ 0.70 ✅ |
| Answer Relevancy | 0.82 | ≥ 0.70 ✅ |
| Context Precision | 0.78 | ≥ 0.70 ✅ |
| Context Recall | 0.80 | ≥ 0.70 ✅ |

### Latencia (p95)

| Endpoint | p95 | KPI |
|---|---|---|
| `/health` | 12ms | < 100ms ✅ |
| `/query` | 1.8s | < 5s ✅ |
| `/analyze` | 18.5s | < 30s ✅ |

### Costos

| Concepto | Costo |
|---|---|
| Por análisis (5 agentes GPT-4o) | ~$0.075 |
| API OpenAI mensual (500 análisis) | ~$37.70 |
| Infraestructura (on-premise) | $0 |

## Inicio Rápido

### 1. Clonar y configurar

```bash
git clone https://gitlab.com/ia/saircp-llm-rag.git
cd saircp-llm-rag
cp .env.example .env
# Editar .env → agregar OPENAI_API_KEY
```

### 2. Ejecutar con Docker Compose (recomendado)

```bash
docker compose up --build -d
# Frontend: http://localhost:3000
# API:      http://localhost:8000/docs
```

### 3. Ejecutar sin Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
cd frontend && python -m http.server 3000
```

### 4. Verificar

```bash
make health
# o: curl http://localhost:8000/api/v1/health
```

## Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v1/health` | GET | Health check |
| `/api/v1/analyze` | POST | Analiza documento (texto) |
| `/api/v1/analyze/upload` | POST | Analiza documento (PDF/DOCX) |
| `/api/v1/ingest` | POST | Ingesta documentos al vector store |
| `/api/v1/query` | POST | Consulta RAG en lenguaje natural |
| `/api/v1/history` | GET | Historial de análisis realizados |

## Arquitectura Multi-Agente

```
Documento → [Analizador] → [Comparador] → [Investigador] → [Evaluador] → [Generador] → Informe
                              ↓ RAG            ↓ RNP/Web         ↓ 13 reglas
                           ChromaDB          Fuentes ext.      Score 0-100
```

El pipeline procesa cada documento con 5 agentes especializados, cada uno con su propio system prompt y schema de salida JSON. El score final (0-100) clasifica el riesgo en BAJO (0-30), MEDIO (31-60), o ALTO (61+).

## Modelo de Scoring (13 indicadores)

| Categoría | Indicador | Peso |
|---|---|---|
| Reglas determinísticas | Marca explícita | 20 |
| Reglas determinísticas | Modelo específico | 20 |
| Reglas determinísticas | Sin "o equivalente" | 15 |
| Reglas determinísticas | Certificación restrictiva | 15 |
| Reglas determinísticas | Experiencia excesiva | 10 |
| Análisis de mercado | Pocos proveedores | 10 |
| Análisis de mercado | Concentración de mercado | 10 |
| Análisis de mercado | Limitación geográfica | 5 |
| Análisis comparativo | Divergencia vs similares | 10 |
| Análisis comparativo | Más restrictivo | 10 |
| Análisis semántico | Similitud con ficha comercial | 15 |
| Análisis semántico | Lenguaje alineado a producto | 10 |
| Análisis semántico | Justificación débil | 10 |

## Comandos (Makefile)

```bash
make help            # Lista todos los comandos
make dev             # Servidor desarrollo con hot-reload
make test            # Pruebas unitarias + integración
make test-cov        # Pruebas con cobertura (≥ 60%)
make test-load       # Prueba de carga (10 usuarios)
make lint            # Ruff + MyPy
make security        # Bandit + pip-audit
make eval            # Evaluación LLM (RAGAS)
make up              # Docker compose up
make pre-delivery    # Validación completa pre-entrega
```

## Documentación

| Documento | Descripción |
|---|---|
| `docs/PROJECT_DOCUMENTATION.md` | Documentación unificada completa (secciones 1-10) |
| `docs/DEMO_EXAMPLES.md` | Ejemplos para la demo |
| `docs/VIDEO_GUIDE.md` | Guía para el video de presentación |
| `docs/adr/ADR-001..003.md` | Architecture Decision Records |
| `docs/api/openapi.yaml` | Especificación OpenAPI 3.1 |
| `REQUIRED_FILES.md` | Checklist de entrega |

## Estructura del Proyecto

```
├── .gitlab-ci.yml          # Pipeline GitLab CI (5 stages)
├── .github/workflows/      # GitHub Actions
├── Dockerfile              # Multi-stage + HEALTHCHECK
├── docker-compose.yml      # 3 servicios (frontend + api + db)
├── Makefile                # 15 comandos documentados
├── src/                    # Código fuente
│   ├── api/routes.py       # 6 endpoints REST
│   ├── agents/             # 5 agentes + orquestador
│   ├── core/               # Config + schemas
│   └── rag/                # Vector store + ingesta + retriever
├── tests/                  # 50+ tests (unit + integration + load)
├── frontend/               # UI institucional OECE
├── scripts/                # Evaluación LLM
├── notebooks/              # Dataset 25 Q/A
├── docs/                   # Documentación completa
└── reports/                # Generados por CI
```

## Licencia

Proyecto académico — AI-LLM Solution Architect  
**Versión:** v1.0.0
