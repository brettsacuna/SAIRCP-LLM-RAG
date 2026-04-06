# ADR-001: Selección del Modelo LLM Base

**Fecha:** 06/04/2026  
**Estado:** Aceptado  
**Autores:** Brett Sacuña

## Contexto

El sistema SAIRCP requiere un modelo de lenguaje capaz de analizar documentos de contratación pública en español, extraer información estructurada (JSON), razonar sobre restricciones legales y generar informes coherentes. Se necesita soporte nativo para JSON mode, baja latencia y capacidad de seguir instrucciones complejas con temperature=0 para reproducibilidad.

## Decisión

Se selecciona **OpenAI GPT-4o** como modelo LLM base del sistema.

## Consecuencias Positivas

- Soporte nativo de `response_format: json_object` que garantiza salidas JSON válidas para el pipeline multi-agente
- Excelente comprensión del español y terminología legal/administrativa peruana
- Latencia competitiva (~1-3s por llamada) compatible con el KPI de p95 < 30s por análisis completo (5 llamadas secuenciales)
- Amplia ventana de contexto (128K tokens) que permite analizar documentos extensos sin truncamiento excesivo
- Ecosistema maduro de SDKs, documentación y tooling (LangSmith, Langfuse)
- Función calling y structured outputs para futuras extensiones con herramientas

## Consecuencias Negativas / Trade-offs

- Dependencia de un proveedor externo (vendor lock-in con OpenAI)
- Costo por token más alto que modelos open-source (~$2.50/1M input, $10/1M output)
- Los datos del documento salen del perímetro institucional (mitigado con política de zero-retention de OpenAI API)
- No es posible hacer fine-tuning de GPT-4o (solo de GPT-4o-mini), lo cual limita la especialización futura

## Alternativas Consideradas

- **Anthropic Claude 3.5 Sonnet:** Rendimiento comparable y mejor en textos largos, pero menor ecosistema en LATAM y pricing similar. Descartado por menor familiaridad del equipo.
- **Google Gemini 1.5 Pro:** Ventana de contexto de 1M tokens, pero menor consistencia en structured outputs JSON y menor precisión en español técnico-legal. Descartado.
- **Meta Llama 3.1 70B (self-hosted):** Eliminaría vendor lock-in y datos salen del perímetro, pero requiere GPU dedicada (~$2-4K/mes), equipo de MLOps y tiempo de setup incompatible con el cronograma MVP de 8 semanas. Descartado para MVP, candidato para fase 2.
- **OpenAI GPT-4o-mini:** 10x más barato pero menor capacidad de razonamiento en análisis complejos y mayor tasa de error en extracción estructurada. Descartado como modelo principal, viable como fallback para consultas simples.
