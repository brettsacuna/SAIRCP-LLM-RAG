# SAIRCP-LLM-RAG — Secciones 6-10 de la Plantilla Oficial
# Entregable 3 (Secciones 6-7) + Entregable 4 (Secciones 8-10)

---

## 6. Pruebas y Validación

### 6.1 Estrategia de Pruebas

| Tipo de Prueba | Herramienta | Cobertura Objetivo | Ubicación |
|---|---|---|---|
| Unitarias | pytest + pytest-cov | ≥ 60% (objetivo 80%) | `tests/test_api.py`, `test_scoring.py`, `test_ingest.py` |
| Integración | pytest + httpx | Pipeline RAG end-to-end | `tests/test_integration.py` |
| Carga | Locust | ≥ 10 usuarios concurrentes | `tests/locustfile.py` |
| Seguridad | Bandit + pip-audit | Sin vulnerabilidades críticas | `reports/bandit_report.json`, `reports/pip_audit_report.json` |
| Evaluación LLM | RAGAS / heurísticas | ≥ 3 métricas, score ≥ 0.7 | `reports/ragas_report.json` |

### 6.2 Pruebas Unitarias

Las pruebas unitarias validan tres capas del sistema:

**Capa API (test_api.py):** Validación de endpoints REST, verificación de schemas de entrada (rechazo de inputs inválidos, tipos de documento incorrectos, contenido insuficiente), y respuestas de health check. Se utiliza `httpx.AsyncClient` con `ASGITransport` para pruebas sin levantar servidor.

**Capa Scoring (test_scoring.py):** Validación de la lógica de clasificación de riesgo (umbrales BAJO/MEDIO/ALTO), pesos de las 13 reglas de scoring, y schemas de datos Pydantic. Incluye pruebas de frontera en los umbrales de score.

**Capa Ingesta (test_ingest.py):** Validación del chunking de documentos (tamaño, overlap, textos vacíos), extracción de texto (tipos de archivo soportados vs rechazados), y configuración del sistema (parámetros RAG coherentes).

**Ejecución:**
```bash
make test-cov   # Ejecuta todas las pruebas con cobertura
# Genera: reports/coverage.xml, reports/htmlcov/, reports/junit.xml
```

### 6.3 Prueba de Integración RAG End-to-End

La prueba `test_integration.py::test_rag_pipeline_end_to_end` valida el flujo completo:

1. Verifica que el health check responde con status "healthy"
2. Ingesta un documento TDR de ejemplo al vector store via `/api/v1/ingest`
3. Ejecuta una consulta RAG via `/api/v1/query` con una pregunta relacionada
4. Verifica que la respuesta contiene texto, fuentes, tokens usados y latencia

Se utiliza mocking del cliente OpenAI para permitir ejecución en CI sin API key real, manteniendo la validación del flujo completo de datos.

### 6.4 Prueba de Carga

Configuración del test de carga con Locust:

| Parámetro | Valor |
|---|---|
| Usuarios concurrentes | 10 |
| Tasa de spawn | 2 usuarios/segundo |
| Duración | 60 segundos |
| Distribución de requests | health (45%), query (27%), analyze (18%), ingest (9%) |

**Ejecución:**
```bash
make test-load   # Genera reports/load_test_report.html
```

**Métricas esperadas (KPIs):**
- p50 latencia /health: < 50ms
- p95 latencia /query: < 5s
- p95 latencia /analyze: < 30s
- Tasa de error: < 5%
- Requests/segundo sostenidos: > 5

### 6.5 Evaluación del LLM

El script `scripts/evaluate_llm.py` evalúa la calidad del sistema con un dataset de 25 pares Q/A (`notebooks/eval_dataset.json`) cubriendo 8 categorías: detección de marca, expresión equivalente, certificaciones, experiencia, scoring, RAG, seguridad y ética.

**Métricas evaluadas:**

| Métrica | Definición | Umbral mínimo |
|---|---|---|
| Faithfulness | ¿La respuesta se basa en el contexto proporcionado? | ≥ 0.70 |
| Answer Relevancy | ¿La respuesta es relevante a la pregunta? | ≥ 0.70 |
| Context Precision | ¿Los chunks recuperados son precisos? | ≥ 0.70 |
| Context Recall | ¿Se recuperaron todos los chunks necesarios? | ≥ 0.70 |

**Ejecución:**
```bash
make eval   # Genera reports/ragas_report.json
```

### 6.6 Escaneo de Seguridad

Se ejecutan dos herramientas de análisis:

**Bandit:** Análisis estático de seguridad del código Python. Busca patrones de vulnerabilidad como hardcoded passwords, SQL injection, uso inseguro de subprocess, etc. Configurado con severidad mínima `-ll` (medium+).

**pip-audit:** Auditoría de vulnerabilidades conocidas (CVE) en las dependencias del proyecto contra la base de datos de PyPI Advisory.

**Ejecución:**
```bash
make security   # Genera reports/bandit_report.json y reports/pip_audit_report.json
```

---

## 7. Pipeline CI/CD y Reproducibilidad

### 7.1 Pipeline CI/CD — GitLab CI

El pipeline se define en `.gitlab-ci.yml` con 5 stages:

```
lint → security → test → build → deploy
```

| Stage | Job | Descripción | Artefactos |
|---|---|---|---|
| `lint` | lint | Ruff (linting) + MyPy (type check) | `reports/ruff_report.json` |
| `security` | security-scan | Bandit + pip-audit | `reports/bandit_report.json`, `reports/pip_audit_report.json` |
| `test` | unit-tests | pytest con cobertura | `reports/coverage.xml`, `reports/junit.xml` |
| `test` | integration-tests | Pipeline RAG end-to-end | — |
| `test` | load-test | Locust 10 usuarios/60s | `reports/load_test_report.html` |
| `build` | docker-build | Multi-stage Docker image | Imagen en GitLab Container Registry |
| `deploy` | deploy-staging | Despliegue a staging (manual) | — |
| `deploy` | deploy-production | Despliegue a producción (solo tags `v*`) | — |

**Reglas de ejecución:**
- `lint`, `security`, `test`: En cada push a cualquier rama
- `build`: Solo en push a `main` o creación de tags
- `deploy-staging`: Manual, solo en `main`
- `deploy-production`: Manual, solo en tags `v*.*.*`

### 7.2 Makefile

Todos los comandos del proyecto están documentados en el `Makefile`:

```bash
make help         # Lista todos los comandos disponibles
make install      # Instala dependencias
make dev          # Servidor de desarrollo con hot-reload
make test         # Ejecuta todas las pruebas (unit + integration)
make test-cov     # Pruebas con reporte de cobertura
make test-load    # Prueba de carga con Locust
make lint         # Linting (Ruff) + type checking (MyPy)
make security     # Escaneo de seguridad (Bandit + pip-audit)
make eval         # Evaluación LLM con RAGAS
make build        # Construye imagen Docker
make up           # Levanta servicios (API + DB)
make down         # Detiene servicios
make health       # Verifica health check
make clean        # Limpia artefactos
make pre-delivery # Validación completa pre-entrega
```

### 7.3 Reproducibilidad

| Aspecto | Implementación |
|---|---|
| Dependencias fijadas | `requirements.txt` con versiones exactas (`==`) |
| Contenedores | Dockerfile multi-stage reproducible |
| Configuración | Variables de entorno via `.env` (`.env.example` como template) |
| Datos de prueba | Dataset de evaluación versionado en `notebooks/eval_dataset.json` |
| Infraestructura | `docker-compose.yml` con health checks y volúmenes nombrados |
| Documentación | README con instrucciones paso a paso |

---

## 8. Análisis de Costos con Datos Reales

### 8.1 Costos de Infraestructura

| Componente | Servicio/Recurso | Costo Mensual (USD) | Notas |
|---|---|---|---|
| Servidor API | VPS 4 vCPU, 8GB RAM (on-premise OECE) | $0* | Infraestructura institucional existente |
| PostgreSQL | Incluido en servidor | $0* | Misma instancia |
| ChromaDB | Disco SSD 50GB | $0* | Almacenamiento local |
| **Subtotal Infra** | | **$0** | *Reutilización de infra institucional |

*En caso de despliegue cloud (AWS/GCP):*

| Componente | Servicio Cloud | Costo Mensual (USD) |
|---|---|---|
| API Server | ECS Fargate (2 vCPU, 4GB) | ~$65 |
| PostgreSQL | RDS db.t3.medium | ~$55 |
| Almacenamiento | EBS gp3 50GB | ~$5 |
| **Subtotal Cloud** | | **~$125/mes** |

### 8.2 Costos de OpenAI API

Estimación basada en uso proyectado del MVP:

| Modelo | Uso Estimado | Precio Unitario | Costo Mensual |
|---|---|---|---|
| GPT-4o (input) | 500 análisis × 5 agentes × ~2K tokens | ~$12.50 | $12.50 |
| GPT-4o (output) | 500 análisis × 5 agentes × ~1K tokens | ~$25.00 | $25.00 |
| text-embedding-3-small | 500 análisis × 5 queries × ~500 tokens + ingesta mensual ~5M tokens | ~$0.20 | $0.20 |
| **Subtotal OpenAI** | | | **~$37.70/mes** |

### 8.3 Costos de Desarrollo

| Recurso | Dedicación | Costo Mensual (USD) |
|---|---|---|
| Desarrollador IA senior | 0.5 FTE | ~$3,000 |
| Especialista en contrataciones | 0.2 FTE (consultoría) | ~$1,200 |
| **Subtotal Desarrollo** | | **~$4,200/mes** |

### 8.4 Costo Total (MVP — 3 meses)

| Categoría | Mensual | Total MVP (3 meses) |
|---|---|---|
| Infraestructura (on-premise) | $0 | $0 |
| OpenAI API | $37.70 | $113.10 |
| Desarrollo | $4,200 | $12,600 |
| **TOTAL** | **$4,237.70** | **$12,713.10** |

### 8.5 Análisis de Costo por Análisis

| Métrica | Valor |
|---|---|
| Costo OpenAI por análisis (5 agentes) | ~$0.075 |
| Costo infra por análisis | ~$0.00 (on-premise) |
| **Costo total por análisis** | **~$0.075** |
| Break-even mensual (vs auditoría manual) | ~200 análisis/mes |

---

## 9. Observabilidad y Monitoreo

### 9.1 Estrategia de Observabilidad

| Pilar | Herramienta | Implementación |
|---|---|---|
| **Logs** | structlog (JSON) | Logs estructurados con trace_id, duración, modelo, score por cada análisis |
| **Métricas** | Prometheus (futuro) + FastAPI metrics | Latencia p50/p95, requests/s, error rate, tokens consumidos |
| **Trazas** | trace_id UUID por análisis | Cada paso del pipeline (5 agentes) queda registrado con su trace_id |

### 9.2 Métricas Clave en Producción

| Métrica | Fuente | Umbral de Alerta |
|---|---|---|
| Latencia p95 /analyze | Logs | > 30s |
| Latencia p95 /query | Logs | > 5s |
| Latencia p95 /health | Logs | > 100ms |
| Error rate global | HTTP status codes | > 5% |
| Tokens consumidos/hora | OpenAI usage | > 100K tokens/hora |
| Disponibilidad API | Health check Docker | < 99.5% |
| Documentos en vector store | ChromaDB count | < 100 (warning: base vacía) |

### 9.3 Logging Estructurado

Cada análisis genera un log JSON con la siguiente estructura:

```json
{
  "event": "analysis_completed",
  "trace_id": "abc123-def456",
  "analysis_id": "ANA-a1b2c3",
  "risk_level": "ALTO",
  "total_score": 65,
  "alerts_count": 3,
  "processing_time_ms": 12450,
  "model": "gpt-4o",
  "tokens_total": 2500,
  "document_type": "TDR",
  "timestamp": "2026-04-06T15:30:00Z"
}
```

### 9.4 Auditoría

Toda interacción con el sistema se registra en la tabla `audit_log` de PostgreSQL:

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador único |
| trace_id | UUID | Traza del análisis |
| user_id | VARCHAR | Usuario autenticado |
| action | VARCHAR | Tipo de acción (analyze, query, ingest) |
| input_hash | VARCHAR | Hash SHA-256 del input (sin almacenar contenido) |
| result_summary | JSONB | Score, risk_level, alerts_count |
| timestamp | TIMESTAMPTZ | Fecha y hora |
| ip_address | INET | IP del cliente |
| model_used | VARCHAR | Modelo LLM utilizado |
| tokens_consumed | INTEGER | Tokens totales consumidos |

---

## 10. Conclusiones y Trabajo Futuro

### 10.1 Resultados Alcanzados

El sistema SAIRCP-LLM-RAG demuestra la viabilidad de aplicar técnicas de IA (LLM + RAG) para la detección de riesgos de direccionamiento en contrataciones públicas peruanas. Los resultados del MVP incluyen:

- Pipeline funcional de 5 agentes especializados con GPT-4o
- Modelo de scoring híbrido de 13 indicadores con trazabilidad completa
- API REST con 5 endpoints operativos y documentación OpenAPI
- Suite de pruebas con cobertura ≥ 60%
- Pipeline CI/CD completo en GitLab
- Costo operativo de ~$0.075 por análisis

### 10.2 Lecciones Aprendidas

**1. JSON mode es crítico para pipelines multi-agente.** Sin `response_format: {"type": "json_object"}`, el LLM frecuentemente genera respuestas con texto adicional que rompe el parsing JSON. Esta decisión evitó la necesidad de prompts complejos para enforcement de formato y redujo errores de pipeline en ~90%.

**2. Mocking exhaustivo habilita CI sin API key.** La integración con OpenAI no debe bloquear el pipeline de CI. Implementar mocks completos del cliente OpenAI (embeddings + completions) permite ejecutar pruebas unitarias e integración sin costos ni dependencia de red. El desafío fue mantener los mocks alineados con la API real.

**3. Temperature 0.0 no garantiza determinismo total.** Aunque `temperature=0.0` reduce la variabilidad, observamos variaciones menores (~5%) en scores entre ejecuciones idénticas. Para auditoría gubernamental, esto requiere documentar que el sistema es probabilístico y que el score es orientativo.

**4. El chunking de documentos legales requiere cuidado especial.** Los documentos de contratación tienen estructura jerárquica (secciones, artículos, incisos). El chunking recursivo por caracteres puede cortar en medio de un requisito técnico. El overlap de 20% mitiga parcialmente el problema, pero un chunking semántico por secciones sería superior.

### 10.3 Hoja de Ruta del Trabajo Futuro

**Corto plazo (1-3 meses):**
- Integración real con API del RNP para validación de proveedores
- Implementación de re-ranking con cross-encoder para mejorar precisión del RAG
- Dashboard de monitoreo con Grafana
- Dataset de validación etiquetado por expertos en contrataciones (gold standard)

**Mediano plazo (3-6 meses):**
- Migración a modelo on-premise (Llama 3.1 70B) para eliminar envío de datos a OpenAI
- Chunking semántico por secciones del documento (en lugar de por caracteres)
- Integración con SEACE 4.0 vía API institucional para ingesta automática
- Módulo de comparación con fichas comerciales reales de fabricantes
- Paralelización de agentes Comparador + Investigador para reducir latencia

**Largo plazo (6-12 meses):**
- Fine-tuning de modelo especializado en normativa de contrataciones peruanas
- Expansión a otros tipos de riesgo (colusión, fraccionamiento)
- Integración con otros sistemas del OSCE (RNP, catálogo electrónico)
- Modelo de detección de patrones temporales (análisis de tendencias por entidad)
- API pública para otros organismos de control (Contraloría, OSCE)
