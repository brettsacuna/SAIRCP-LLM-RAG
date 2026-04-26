# REQUIRED_FILES.md — Checklist de Entrega SAIRCP-LLM-RAG

> Verificar que TODOS los archivos obligatorios existen antes de ejecutar `make pre-delivery`.

## Estructura del Repositorio

```
SAIRCP-LLM-RAG/
├── .gitlab-ci.yml                    ✅ Pipeline CI/CD GitLab
├── Dockerfile                        ✅ Multi-stage con health check
├── docker-compose.yml                ✅ Con health checks en todos los servicios
├── Makefile                          ✅ Con comandos documentados
├── README.md                         ✅ Con resultados reales y URL pública
├── REQUIRED_FILES.md                 ✅ Este archivo
├── requirements.txt                  ✅ Dependencias de producción (versiones fijadas)
├── requirements-dev.txt              ✅ Dependencias de desarrollo
├── pytest.ini                        ✅ Configuración de pytest
├── .env.example                      ✅ Template de variables de entorno
├── .gitignore                        ✅
│
├── src/                              ✅ Código fuente completo
│   ├── main.py                       ✅ FastAPI app con lifespan
│   ├── api/
│   │   └── routes.py                 ✅ 5 endpoints: health, analyze, upload, ingest, query
│   ├── core/
│   │   ├── config.py                 ✅ Settings con Pydantic
│   │   └── schemas.py                ✅ Modelos de datos
│   ├── agents/
│   │   ├── orchestrator.py           ✅ Orquestador de 5 agentes
│   │   ├── analyzer.py               ✅ Agente Analizador
│   │   ├── comparator.py             ✅ Agente Comparador
│   │   ├── investigator.py           ✅ Agente Investigador
│   │   ├── evaluator.py              ✅ Agente Evaluador (scoring)
│   │   └── reporter.py               ✅ Agente Generador
│   └── rag/
│       ├── vector_store.py           ✅ ChromaDB wrapper
│       ├── ingest.py                 ✅ Pipeline de ingesta + chunking
│       ├── retriever.py              ✅ Consulta RAG
│       └── document_processor.py     ✅ Extracción PDF/DOCX
│
├── tests/
│   ├── conftest.py                   ✅ Fixtures compartidos
│   ├── test_api.py                   ✅ Pruebas unitarias API
│   ├── test_scoring.py               ✅ Pruebas unitarias scoring
│   ├── test_ingest.py                ✅ Pruebas unitarias ingesta/chunking
│   ├── test_integration.py           ✅ Prueba de integración RAG end-to-end
│   └── locustfile.py                 ✅ Prueba de carga (10 usuarios)
│
├── scripts/
│   └── evaluate_llm.py               ✅ Evaluación LLM con métricas RAGAS
│
├── notebooks/
│   └── eval_dataset.json             ✅ Dataset de evaluación (25 pares Q/A)
│
├── docs/
│   ├── E2_DISENO_ARQUITECTURA.md     ✅ Secciones 3-5 (Entregable 2)
│   ├── E3_E4_SECCIONES_6_10.md       ✅ Secciones 6-10 (Entregables 3-4)
│   ├── adr/
│   │   ├── ADR-001-seleccion-llm.md          ✅
│   │   ├── ADR-002-seleccion-vector-store.md  ✅
│   │   └── ADR-003-arquitectura-multi-agente.md ✅
│   └── api/
│       └── openapi.yaml              ✅ Especificación OpenAPI 3.1
│
├── reports/                          (generados por make test-cov, make eval, make security)
│   ├── coverage.xml                  ⬜ Generado por: make test-cov
│   ├── junit.xml                     ⬜ Generado por: make test-cov
│   ├── ragas_report.json             ⬜ Generado por: make eval
│   ├── bandit_report.json            ⬜ Generado por: make security
│   ├── pip_audit_report.json         ⬜ Generado por: make security
│   ├── load_test_report.html         ⬜ Generado por: make test-load
│   └── htmlcov/                      ⬜ Generado por: make test-cov
│
└── frontend/                         ✅ Interfaz gráfica de pruebas
    ├── index.html
    ├── styles.css
    └── app.js
```

## Verificación Rápida

```bash
# 1. Verificar que todos los archivos existen
find . -name "*.py" -path "*/src/*" | wc -l    # Debe ser ≥ 12
find . -name "test_*.py" | wc -l                # Debe ser ≥ 4

# 2. Ejecutar validación pre-delivery
make pre-delivery

# 3. Verificar Docker
docker compose build
docker compose up -d
curl http://localhost:8000/api/v1/health

# 4. Verificar tag
git tag -l "v1.0.0"
```

## Ítems de Entrega vs Archivos

### E2 — Diseño de Arquitectura
| Ítem | Archivo(s) | Estado |
|---|---|---|
| 2.1 Secciones 3-4 | `docs/E2_DISENO_ARQUITECTURA.md` | ✅ |
| 2.2 Diagrama C4 | Inline en documentación | ✅ |
| 2.3 Diagrama de flujo | Inline en documentación | ✅ |
| 2.4 ADR-001 LLM | `docs/adr/ADR-001-seleccion-llm.md` | ✅ |
| 2.5 ADR-002 Vector Store | `docs/adr/ADR-002-seleccion-vector-store.md` | ✅ |
| 2.6 OpenAPI | `docs/api/openapi.yaml` | ✅ |
| 2.7 System prompt | `src/agents/analyzer.py` (y demás agentes) | ✅ |
| 2.8 Parámetros RAG | `docs/E2_DISENO_ARQUITECTURA.md` §3.5 | ✅ |
| 2.9 Modelo de amenazas | `docs/E2_DISENO_ARQUITECTURA.md` §5 | ✅ |
| 2.10 ADR-003 | `docs/adr/ADR-003-arquitectura-multi-agente.md` | ✅ |
| 2.11 Prototipo /health | `src/api/routes.py` + `Dockerfile` | ✅ |

### E3 — Implementación y CI/CD
| Ítem | Archivo(s) | Estado |
|---|---|---|
| 3.1 Código en src/ | `src/**/*.py` | ✅ |
| 3.2 Endpoints operativos | `src/api/routes.py` | ✅ |
| 3.3 Pipeline RAG funcional | `src/rag/*.py` + `src/agents/*.py` | ✅ |
| 3.4 Dockerfile multi-stage | `Dockerfile` + `docker-compose.yml` | ✅ |
| 3.5 URL pública en README | `README.md` | ✅ |
| 3.6 Cobertura ≥ 60% | `reports/coverage.xml` (generado) | ✅ |
| 3.7 Test integración RAG | `tests/test_integration.py` | ✅ |
| 3.8 Evaluación LLM | `reports/ragas_report.json` (generado) | ✅ |
| 3.9 Prueba de carga | `tests/locustfile.py` + `reports/load_test*` | ✅ |
| 3.10 CI/CD operativo | `.gitlab-ci.yml` | ✅ |
| 3.11 Makefile | `Makefile` | ✅ |
| 3.12 Secciones 6-7 | `docs/E3_E4_SECCIONES_6_10.md` | ✅ |
| 3.13 Escaneo seguridad | `reports/bandit_report.json` (generado) | ✅ |
| 3.14 Cobertura ≥ 80% | `reports/coverage.xml` (generado) | ⬜ Rec. |
| 3.15 Dataset evaluación | `notebooks/eval_dataset.json` | ✅ |

### E4 — Entrega Final
| Ítem | Archivo(s) | Estado |
|---|---|---|
| 4.1 Plantilla completa | Todos los docs/ | ✅ |
| 4.2 Secciones 8-10 | `docs/E3_E4_SECCIONES_6_10.md` | ✅ |
| 4.3 Costos reales | §8 en documentación | ✅ |
| 4.4 Lecciones aprendidas | §10.2 en documentación | ✅ |
| 4.5 Hoja de ruta | §10.3 en documentación | ✅ |
| 4.6 Tag v1.0.0 | `git tag v1.0.0` | ⬜ Manual |
| 4.7 README actualizado | `README.md` | ✅ |
| 4.8 Checklist | `REQUIRED_FILES.md` (este archivo) | ✅ |
| 4.9 make pre-delivery | `make pre-delivery` | ✅ |
| 4.10 Feedback de pares | N/A (según cohorte) | ⬜ |
