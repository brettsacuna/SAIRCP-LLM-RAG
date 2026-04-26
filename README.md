# SAIRCP-LLM-RAG

**Sistema de Apoyo para la Identificación de Riesgos en Contrataciones Públicas mediante IA**  
Extensión del SEACE 4.0 — OECE

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Python 3.11 + FastAPI |
| LLM | OpenAI GPT-4o |
| Embeddings | text-embedding-3-small |
| Vector Store | ChromaDB |
| Base de Datos | PostgreSQL 16 |
| Contenedores | Docker + Docker Compose |

## Resultados Reales

### Métricas LLM (RAGAS)

| Métrica | Score | Umbral |
|---|---|---|
| Faithfulness | 0.85 | ≥ 0.70 ✅ |
| Answer Relevancy | 0.82 | ≥ 0.70 ✅ |
| Context Precision | 0.78 | ≥ 0.70 ✅ |
| Context Recall | 0.80 | ≥ 0.70 ✅ |

### Latencia (p95)

| Endpoint | Latencia p95 | KPI |
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
git clone https://github.com/brettsacuna/SAIRCP-LLM-RAG.git
cd SAIRCP-LLM-RAG
cp .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY
```

### 2. Ejecutar con Docker Compose

```bash
docker compose up --build
```

### 3. Ejecutar sin Docker (desarrollo local)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### 4. Verificar

```bash
curl http://localhost:8000/api/v1/health
```

### 5. Ejecutar el frontend

```bash
cd frontend && python -m http.server 3000
```

## Endpoints Principales

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v1/health` | GET | Health check |
| `/api/v1/analyze` | POST | Analiza documento (texto) |
| `/api/v1/analyze/upload` | POST | Analiza documento (PDF/DOCX) |
| `/api/v1/ingest` | POST | Ingesta documentos al vector store |
| `/api/v1/query` | POST | Consulta RAG en lenguaje natural |

## Documentación API

Con el servidor corriendo: [http://localhost:8000/docs](http://localhost:8000/docs)

## Tests

```bash
pytest tests/ -v
```

## Arquitectura

El sistema utiliza una arquitectura multi-agente con 5 agentes especializados:

1. **Analizador** — Extrae requisitos y restricciones del documento
2. **Comparador** — Contrasta con procesos similares (RAG/SEACE)
3. **Investigador** — Consulta RNP y fuentes web
4. **Evaluador** — Calcula scoring de riesgo (reglas + IA)
5. **Generador** — Produce informe final con evidencia trazable

## Comandos (Makefile)

```bash
make help            # Lista todos los comandos
make test            # Pruebas unitarias + integración
make test-cov        # Pruebas con cobertura (≥ 60%)
make test-load       # Prueba de carga (10 usuarios)
make lint            # Linting + type checking
make security        # Bandit + pip-audit
make eval            # Evaluación LLM (RAGAS)
make pre-delivery    # Validación completa pre-entrega

## Licencia

Proyecto académico — AI-LLM Solution Architect
