"""
Prueba de carga — Locust
Simula ≥ 10 usuarios concurrentes contra los endpoints del SAIRCP.

Ejecutar:
  locust -f tests/locustfile.py --headless --users 10 --spawn-rate 2 \
    --run-time 60s --host http://localhost:8000 --csv=reports/load_test \
    --html=reports/load_test_report.html
"""

from locust import HttpUser, task, between


class SAIRCPUser(HttpUser):
    """Simula un usuario del sistema SAIRCP."""

    wait_time = between(1, 3)

    @task(5)
    def health_check(self):
        """Health check — endpoint más frecuente."""
        self.client.get("/api/v1/health")

    @task(3)
    def query_rag(self):
        """Consulta RAG de lenguaje natural."""
        self.client.post("/api/v1/query", json={
            "query": "¿Cuáles son los requisitos comunes en TDR de servidores?",
            "top_k": 5
        })

    @task(2)
    def analyze_document(self):
        """Análisis de documento de contratación."""
        self.client.post("/api/v1/analyze", json={
            "content": (
                "TÉRMINOS DE REFERENCIA — Adquisición de Equipos de Cómputo. "
                "Se requiere la adquisición de 10 computadoras de escritorio "
                "marca HP ProDesk 400 G9 con procesador Intel Core i7-12700, "
                "16GB RAM DDR5, disco SSD 512GB NVMe, monitor 24 pulgadas. "
                "El proveedor debe contar con certificación ISO 9001 vigente. "
                "Experiencia mínima de 3 años en venta de equipos informáticos "
                "al sector público peruano. Plazo de entrega: 20 días calendario."
            ),
            "document_type": "TDR"
        })

    @task(1)
    def ingest_document(self):
        """Ingesta de un documento de referencia."""
        self.client.post("/api/v1/ingest", json={
            "documents": [{
                "content": (
                    "Proceso de referencia: Adquisición de laptops para OECE. "
                    "Se adquirieron 20 laptops Lenovo ThinkPad L14 Gen 3 con "
                    "procesador AMD Ryzen 5 5625U. Monto adjudicado: S/ 150,000."
                ),
                "metadata": {
                    "type": "referencia",
                    "year": 2025,
                    "entity": "OECE"
                }
            }]
        })
