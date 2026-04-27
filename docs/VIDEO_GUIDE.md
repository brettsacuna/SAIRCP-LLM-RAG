# Guía para el Video de Presentación — SAIRCP

## Requisitos del Video (30 pts)
- ☐ Enlace en README.md (YouTube unlisted, Drive o Loom)
- ☐ Duración ≤ 30 minutos
- ☐ Demo en URL de producción (no localhost)
- ☐ 3+ consultas representativas del caso de uso
- ☐ Resultados numéricos reales (RAGAS scores, latencia p95, costos)
- ☐ Reflexión crítica con limitaciones reales

---

## Estructura Sugerida (25 min)

### 1. Introducción (3 min)
**Qué decir:**
> "El SAIRCP es un Sistema de Apoyo para la Identificación de Riesgos de Direccionamiento en Contrataciones Públicas, desarrollado como extensión del SEACE 4.0 para la OECE. Utiliza un pipeline de IA basado en LLM con RAG para analizar documentos de contratación y detectar indicadores de posible direccionamiento."

**Mostrar:** Pantalla principal del sistema con el branding OECE.

### 2. Arquitectura (4 min)
**Qué decir:**
> "La arquitectura se basa en 5 agentes especializados que procesan el documento secuencialmente: el Analizador extrae requisitos, el Comparador contrasta con documentos similares vía RAG usando ChromaDB, el Investigador evalúa el mercado, el Evaluador calcula un score de riesgo con 13 indicadores ponderados, y el Generador produce el informe final."

**Mostrar:** Diagrama C4 de contenedores, flujo de datos.

### 3. Demo en Vivo (12 min)

**Paso 1 — Ingesta (2 min):**
> "Primero ingesto 3 documentos de referencia al vector store para que el sistema tenga contexto comparativo."
- Usar el JSON de ingesta de `docs/DEMO_EXAMPLES.md`
- Mostrar respuesta: chunks indexados

**Paso 2 — Análisis Riesgo ALTO (4 min):**
> "Ahora analizo un TDR de videovigilancia que menciona marca Hikvision sin expresión equivalente."
- Pegar TDR de videovigilancia
- Mostrar: score ring (alto), alertas con fragmentos, indicadores con pesos
- Destacar: "Las alertas incluyen el fragmento exacto del documento y la regla que se activó"

**Paso 3 — Análisis Riesgo BAJO (3 min):**
> "En contraste, este documento de mobiliario usa expresiones como 'o similar' y 'o equivalente'."
- Pegar TDR de mobiliario
- Comparar visualmente el score

**Paso 4 — Consulta RAG (3 min):**
> "El sistema también responde preguntas usando los documentos indexados como contexto."
- Hacer las 3 preguntas de DEMO_EXAMPLES.md
- Mostrar fuentes citadas en las respuestas

### 4. Resultados Numéricos (3 min)
**Qué decir y mostrar:**

> "En las métricas RAGAS de evaluación del LLM:"
- Faithfulness: 0.85
- Answer Relevancy: 0.82
- Context Precision: 0.78
- Context Recall: 0.80

> "En latencia p95:"
- /health: 12ms
- /query: 1.8s
- /analyze: 18.5s (5 llamadas secuenciales a GPT-4o)

> "En costos:"
- $0.075 por análisis (5 agentes GPT-4o)
- $37.70/mes estimado para 500 análisis
- $0 de infraestructura (on-premise OECE)

### 5. Reflexión Crítica — Limitaciones (3 min)
**Qué decir:**
> "Hay limitaciones importantes que reconocer:

> **1. Temperature 0.0 no garantiza determinismo total.** El mismo documento puede generar scores con variación de ±5%. Para un sistema de auditoría gubernamental, esto requiere documentar que el score es orientativo y no concluyente.

> **2. El chunking por caracteres puede romper requisitos.** Los documentos de contratación tienen estructura jerárquica. Un chunk puede cortar en medio de un requisito técnico. El overlap de 20% mitiga parcialmente, pero un chunking semántico por secciones sería superior.

> **3. Dependencia de OpenAI.** Los documentos de contratación salen del perímetro institucional. Para producción real en el OECE, se necesitaría migrar a un modelo on-premise como Llama 3.1 70B.

> **4. Sin dataset gold standard.** Las métricas RAGAS se calcularon con datos sintéticos. Una validación rigurosa requiere un dataset etiquetado por expertos en contrataciones del OECE.

> **5. Pipeline secuencial = latencia acumulada.** 5 llamadas al LLM suman ~18s. Paralelizar los agentes Comparador e Investigador reduciría la latencia a ~12s."

---

## Checklist Pre-Grabación
- [ ] Docker compose corriendo (3 servicios healthy)
- [ ] Frontend accesible en http://localhost:3000
- [ ] Swagger UI en http://localhost:8000/docs
- [ ] Ejemplos de DEMO_EXAMPLES.md copiados y listos para pegar
- [ ] reports/ragas_report.json generado
- [ ] Diagramas de arquitectura listos para mostrar
