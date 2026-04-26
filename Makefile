# ===========================================
# SAIRCP-LLM-RAG — Makefile
# ===========================================
# Uso: make <comando>
# Ver todos los comandos disponibles: make help

.PHONY: help install dev test test-unit test-integration test-cov test-load \
        lint security build up down logs health clean eval pre-delivery

SHELL := /bin/bash
PYTHON := python3
PIP := pip
PYTEST := pytest
DOCKER := docker compose
COVERAGE_MIN := 60

# Colores
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m

help: ## Muestra esta ayuda
	@echo ""
	@echo "  SAIRCP-LLM-RAG — Comandos disponibles"
	@echo "  ======================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# --- Setup ---
install: ## Instala dependencias del proyecto
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

dev: ## Inicia servidor de desarrollo con hot-reload
	uvicorn src.main:app --reload --port 8000

# --- Testing ---
test: test-unit test-integration ## Ejecuta todas las pruebas

test-unit: ## Ejecuta pruebas unitarias
	@echo "$(YELLOW)🧪 Ejecutando pruebas unitarias...$(NC)"
	$(PYTEST) tests/test_api.py tests/test_scoring.py tests/test_ingest.py -v

test-integration: ## Ejecuta pruebas de integración RAG end-to-end
	@echo "$(YELLOW)🔗 Ejecutando pruebas de integración...$(NC)"
	$(PYTEST) tests/test_integration.py -v --tb=short

test-cov: ## Ejecuta pruebas con reporte de cobertura
	@echo "$(YELLOW)📊 Ejecutando pruebas con cobertura...$(NC)"
	@mkdir -p reports
	$(PYTEST) tests/ -v \
		--cov=src \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=html:reports/htmlcov \
		--cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_MIN) \
		--junitxml=reports/junit.xml
	@echo "$(GREEN)✅ Reporte en reports/coverage.xml y reports/htmlcov/$(NC)"

test-load: ## Ejecuta prueba de carga con Locust (10 usuarios, 60s)
	@echo "$(YELLOW)📊 Ejecutando prueba de carga...$(NC)"
	@mkdir -p reports
	locust -f tests/locustfile.py \
		--headless \
		--users 10 \
		--spawn-rate 2 \
		--run-time 60s \
		--host http://localhost:8000 \
		--csv=reports/load_test \
		--html=reports/load_test_report.html
	@echo "$(GREEN)✅ Reporte en reports/load_test_report.html$(NC)"

# --- Quality ---
lint: ## Ejecuta linting con Ruff y type-checking con MyPy
	@echo "$(YELLOW)🔍 Linting...$(NC)"
	ruff check src/ --fix
	ruff format src/
	mypy src/ --ignore-missing-imports || true
	@echo "$(GREEN)✅ Lint completado$(NC)"

security: ## Ejecuta escaneo de seguridad (Bandit + pip-audit)
	@echo "$(YELLOW)🛡️ Escaneo de seguridad...$(NC)"
	@mkdir -p reports
	bandit -r src/ -f json -o reports/bandit_report.json || true
	bandit -r src/ -ll
	pip-audit --format=json --output=reports/pip_audit_report.json || true
	pip-audit
	@echo "$(GREEN)✅ Reportes en reports/$(NC)"

# --- Evaluation ---
eval: ## Ejecuta evaluación del LLM con RAGAS y genera reporte
	@echo "$(YELLOW)🤖 Ejecutando evaluación LLM...$(NC)"
	@mkdir -p reports
	$(PYTHON) scripts/evaluate_llm.py
	@echo "$(GREEN)✅ Reporte en reports/ragas_report.json$(NC)"

# --- Docker ---
build: ## Construye la imagen Docker multi-stage
	$(DOCKER) build --no-cache
	@echo "$(GREEN)✅ Imagen construida$(NC)"

up: ## Levanta todos los servicios (API + DB)
	$(DOCKER) up -d --build
	@echo "$(YELLOW)⏳ Esperando health checks...$(NC)"
	@sleep 10
	@$(MAKE) health

down: ## Detiene todos los servicios
	$(DOCKER) down -v
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

logs: ## Muestra logs de los servicios
	$(DOCKER) logs -f --tail=100

health: ## Verifica el health check de la API
	@curl -sf http://localhost:8000/api/v1/health | python3 -m json.tool && \
		echo "$(GREEN)✅ API healthy$(NC)" || \
		echo "$(RED)❌ API no responde$(NC)"

# --- Cleanup ---
clean: ## Limpia artefactos generados
	rm -rf reports/ .pytest_cache/ __pycache__ .mypy_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# --- Pre-delivery ---
pre-delivery: clean lint test-cov security ## Ejecuta validación completa pre-entrega
	@echo ""
	@echo "$(GREEN)=============================================$(NC)"
	@echo "$(GREEN)  ✅ PRE-DELIVERY CHECK PASSED$(NC)"
	@echo "$(GREEN)=============================================$(NC)"
	@echo "  - Lint:       OK"
	@echo "  - Tests:      OK"
	@echo "  - Coverage:   ≥ $(COVERAGE_MIN)%"
	@echo "  - Security:   OK"
	@echo "$(GREEN)=============================================$(NC)"
