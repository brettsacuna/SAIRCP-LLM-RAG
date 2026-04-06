# ADR-003: Arquitectura Multi-Agente Secuencial

**Fecha:** 06/04/2026  
**Estado:** Aceptado  
**Autores:** Brett Sacuña

## Contexto

El análisis de riesgo de un documento de contratación involucra múltiples pasos cognitivos: extracción de requisitos, comparación con históricos, investigación de mercado, evaluación de scoring y generación de informe. Se debe decidir si esto se implementa como un único prompt monolítico, una cadena LangChain, o una arquitectura de agentes especializados.

## Decisión

Se implementa una **arquitectura multi-agente secuencial con 5 agentes especializados**, cada uno con su propio system prompt y responsabilidad única, orquestados por un componente central (`AgentOrchestrator`).

Agentes: Analizador → Comparador → Investigador → Evaluador → Generador.

## Consecuencias Positivas

- **Explicabilidad:** cada paso del análisis es independiente, auditable y trazable
- **Mantenibilidad:** se puede modificar un agente sin afectar los demás
- **Testabilidad:** cada agente se puede probar unitariamente con inputs/outputs fijos
- **Calidad:** prompts especializados producen mejores resultados que un prompt monolítico largo
- **Extensibilidad:** se pueden agregar agentes nuevos (ej: agente normativo) sin reestructurar

## Consecuencias Negativas / Trade-offs

- **Latencia acumulada:** 5 llamadas secuenciales al LLM (~5-15s total vs ~3-5s con prompt único)
- **Costo:** 5x más tokens consumidos por análisis comparado con enfoque monolítico
- **Complejidad:** mayor código de orquestación y manejo de errores entre agentes
- **Propagación de errores:** un error en el agente 1 puede degradar toda la cadena

## Alternativas Consideradas

- **Prompt monolítico único:** Una sola llamada con un prompt extenso. Más rápido y barato, pero imposible de debuggear, propenso a alucinaciones en tareas complejas, y sin trazabilidad por paso. Descartado.
- **LangChain LCEL chains:** Cadenas declarativas con LangChain. Agrega dependencia pesada, abstracción innecesaria sobre la API de OpenAI, y dificultad para debugging. Descartado por over-engineering en esta fase.
- **Agentes paralelos con merge:** Ejecutar agentes 2-4 en paralelo. Reduce latencia pero complica la lógica cuando el Comparador y el Investigador necesitan outputs del Analizador. Candidato para optimización futura.
