# DOCUMENTO TÉCNICO
## Sistema de Apoyo para la Identificación de Riesgos en Contrataciones Públicas mediante Inteligencia Artificial
### Extensión del SEACE 4.0 – OECE

---

# 1. INTRODUCCIÓN

El Organismo Especializado para las Contrataciones Públicas Eficientes (OECE) propone la implementación de un sistema basado en Inteligencia Artificial (IA) como extensión del SEACE 4.0, orientado a la identificación de riesgos en documentos de contratación pública.

El sistema permitirá analizar automáticamente documentos clave del proceso de contratación, tales como términos de referencia (TDR), bases administrativas, especificaciones técnicas y estudios de mercado, con el fin de detectar posibles restricciones a la competencia y generar alertas con evidencia trazable para la toma de decisiones.

Esta iniciativa se orienta a fortalecer el control preventivo, mejorar la transparencia y contribuir a la estandarización del análisis de documentos de contratación pública dentro del ecosistema del SEACE 4.0.

---

# 2. DOCUMENTO DE ALCANCE DEL PROYECTO

## 2.1 Problema

Actualmente, la evaluación de documentos de contratación pública se realiza de manera mayormente manual, lo que dificulta la identificación oportuna de riesgos de direccionamiento, afectando la transparencia, la pluralidad de proveedores y la competencia en los procesos de contratación.

Esta situación incrementa la carga operativa de revisión, limita la capacidad de análisis comparativo con procesos previos y puede originar observaciones posteriores por parte de órganos de control, debido a la inclusión de requisitos técnicos, comerciales o documentales potencialmente restrictivos.

## 2.2 Objetivo

Implementar un sistema basado en Inteligencia Artificial, como extensión funcional del SEACE 4.0, que permita identificar de manera automatizada riesgos de direccionamiento en documentos de contratación pública, generando alertas con evidencia trazable y mecanismos de apoyo a la toma de decisiones.

## 2.3 5W + H

### 2.3.1 WHAT (¿Qué?)

El proyecto consiste en la implementación de un sistema inteligente que permita analizar documentos de contratación pública, identificar patrones de riesgo relacionados con restricciones a la competencia y generar reportes automatizados con soporte documental y trazabilidad.

El sistema analizará documentos como términos de referencia, especificaciones técnicas, bases administrativas y estudios de mercado, mediante técnicas de procesamiento de lenguaje natural, modelos de lenguaje y mecanismos de recuperación de información.

### 2.3.2 WHY (¿Por qué?)

La iniciativa responde a la necesidad de fortalecer el control preventivo en la formulación de requerimientos técnicos y documentos de contratación, donde pueden presentarse condiciones que limiten la libre competencia o reduzcan la pluralidad de proveedores.

Asimismo, busca mejorar la eficiencia operativa del análisis documental, estandarizar criterios de revisión y contribuir a la transparencia del sistema de contrataciones públicas.

### 2.3.3 WHO (¿Quién?)

La Dirección del SEACE del OECE será el órgano responsable del liderazgo funcional del sistema, incluyendo la gobernanza del módulo, la definición de reglas de negocio y la supervisión de su operación.

La Oficina de Tecnologías de la Información participará en la implementación técnica, despliegue, seguridad, interoperabilidad y sostenibilidad de la solución. Las entidades públicas usuarias del SEACE utilizarán el módulo como herramienta de apoyo en la revisión de documentos, mientras que los resultados podrán servir como insumo complementario para instancias de supervisión y control.

### 2.3.4 WHERE (¿Dónde?)

El sistema será implementado como un módulo integrado al SEACE 4.0, desplegado sobre la infraestructura tecnológica institucional del OECE, ya sea en entorno on-premise, nube híbrida o una arquitectura compatible con los lineamientos de interoperabilidad y seguridad institucional.

### 2.3.5 WHEN (¿Cuándo?)

La implementación se plantea por fases, iniciando con la definición de alcance, requerimientos y arquitectura, seguida del desarrollo del producto mínimo viable, integración con fuentes relevantes, pruebas, piloto y despliegue progresivo.

Se estima una duración inicial de ocho semanas para la versión entregable del proyecto académico/documental, con posibilidad de ampliación en una implementación institucional real.

### 2.3.6 HOW (¿Cómo?)

El sistema será implementado como una extensión del SEACE 4.0, utilizando una arquitectura basada en módulos de análisis documental, motores de búsqueda, agentes de IA, mecanismos de scoring de riesgo y componentes de generación de informes.

El flujo general contemplará la carga o lectura del documento desde el SEACE, su análisis automático, la búsqueda y comparación con fuentes relevantes, la identificación de patrones de riesgo y la generación de un informe con alertas, evidencia y trazabilidad.

## 2.4 Alcance y Delimitación

Definición precisa de lo que está dentro y fuera del alcance de la versión entregada.

| ✅ EN SCOPE | ❌ OUT OF SCOPE |
|------------|---------------|
| Integración del módulo de Inteligencia Artificial como extensión del SEACE 4.0 | Determinación automática de actos de corrupción o ilegalidad |
| Análisis automático de documentos de contratación (TDR, bases administrativas, especificaciones técnicas y estudios de mercado) | Aplicación de sanciones o bloqueo de procesos de contratación |
| Procesamiento de lenguaje natural para identificación de requisitos, restricciones y condiciones técnicas | Reemplazo de la evaluación humana en la toma de decisiones |
| Detección de patrones de riesgo como marca, modelo, certificaciones restrictivas y exigencias desproporcionadas | Entrenamiento de modelos de IA desde cero o fine-tuning base en esta fase |
| Consulta de procesos históricos y documentación comparable dentro del SEACE | Acceso a información privada, confidencial o no pública |
| Integración con el Registro Nacional de Proveedores (RNP) para identificar potenciales proveedores | Integración con sistemas externos no oficiales o no autorizados |
| Búsqueda en fuentes web abiertas nacionales para validación de disponibilidad de proveedores | Soporte multilenguaje distinto al español en esta fase |
| Implementación de un motor de scoring de riesgo con categorías bajo, medio y alto | Analítica predictiva avanzada sobre comportamiento futuro de proveedores |
| Generación de informes automatizados con evidencia trazable y justificación del resultado | Automatización completa del proceso de contratación pública |
| Visualización de alertas dentro del flujo del SEACE antes de la publicación del proceso | Integración con sistemas internacionales de contratación o proveedores |
| Registro de auditoría de análisis realizados, usuarios, fechas y resultados | Uso de datos sensibles sin mecanismos de anonimización y control |
| Implementación sobre infraestructura institucional compatible con OECE | Personalización avanzada por entidad en esta primera versión |
| Cumplimiento de lineamientos de seguridad, trazabilidad y gobierno digital | Dependencia obligatoria de modelos propietarios sin control institucional |

## 2.5 Indicadores Clave de Éxito (KPIs del Proyecto)

| KPI / Métrica | Línea Base | Meta Objetivo | Resultado Obtenido |
|--------------|-----------|--------------|--------------------|
| Latencia promedio de análisis (p95) | N/A | < 30 segundos | Completar al final |
| Tasa de detección de riesgos | Baseline inicial | > 85% | Completar al final |
| Precisión en identificación de requisitos | Baseline inicial | > 85% | Completar al final |
| Cobertura de análisis de documentos (%) | 0% | > 90% | Completar al final |
| Tasa de generación de informes exitosos | N/A | 100% | Completar al final |
| Disponibilidad del sistema | N/A | ≥ 99.5% | Completar al final |
| Tiempo de respuesta en consultas externas | N/A | < 5 segundos | Completar al final |
| Nivel de satisfacción de usuario | N/A | > 85% | Completar al final |
| Porcentaje de alertas con evidencia trazable | N/A | 100% | Completar al final |
| Reducción de observaciones en procesos | Baseline institucional | > 20% | Completar al final |

---

# 3. LISTA DE REQUERIMIENTOS TÉCNICOS Y FUNCIONALES

## 3.1 Requerimientos Funcionales

| ID | Descripción del Requerimiento | Prioridad | Criterio de Aceptación |
|----|-------------------------------|-----------|------------------------|
| RF-001 | El sistema debe permitir la carga de documentos de contratación pública en formatos PDF y DOCX. | Alta | El documento se carga y procesa correctamente en el 100% de los casos de prueba definidos. |
| RF-002 | El sistema debe analizar automáticamente el contenido del documento utilizando procesamiento de lenguaje natural. | Alta | El sistema identifica correctamente al menos el 85% de secciones clave del documento en el conjunto de validación. |
| RF-003 | El sistema debe identificar requisitos técnicos, comerciales y documentales dentro del contenido cargado. | Alta | El sistema extrae correctamente al menos el 85% de requisitos presentes en los casos de prueba. |
| RF-004 | El sistema debe detectar posibles restricciones a la competencia, tales como referencias a marcas, modelos específicos o certificaciones restrictivas. | Alta | El sistema detecta al menos el 80% de patrones restrictivos contenidos en el dataset de prueba. |
| RF-005 | El sistema debe identificar la presencia de términos potencialmente direccionados o lenguaje alineado a fichas comerciales. | Alta | El sistema marca coincidencias relevantes en al menos el 75% de los casos de prueba evaluados. |
| RF-006 | El sistema debe integrarse con el SEACE para consultar procesos de contratación similares o comparables. | Alta | La recuperación de procesos comparables se realiza exitosamente en al menos el 85% de los escenarios de prueba. |
| RF-007 | El sistema debe consultar el Registro Nacional de Proveedores (RNP) para identificar proveedores potenciales relacionados con el requerimiento. | Alta | El sistema obtiene resultados pertinentes en al menos el 80% de las consultas de prueba. |
| RF-008 | El sistema debe realizar búsqueda en fuentes web abiertas nacionales para validar disponibilidad de bienes, servicios o proveedores vinculados al requerimiento. | Media | La búsqueda devuelve información útil y relevante en al menos el 75% de las consultas definidas. |
| RF-009 | El sistema debe calcular un score de riesgo a partir de reglas de negocio, análisis de mercado y evaluación semántica basada en IA. | Alta | El score se genera en el 100% de los análisis ejecutados sobre documentos válidos. |
| RF-010 | El sistema debe clasificar el nivel de riesgo en categorías bajo, medio o alto. | Alta | La clasificación se muestra correctamente en el 100% de los análisis realizados. |
| RF-011 | El sistema debe generar un informe automatizado con alertas, score y evidencia asociada. | Alta | El informe se genera correctamente en el 100% de los casos válidos de prueba. |
| RF-012 | El sistema debe mostrar evidencia trazable para cada alerta generada, incluyendo fragmentos de texto resaltados y fuentes consultadas. | Alta | Al menos el 90% de las alertas generadas presenta evidencia verificable y visible para el usuario. |
| RF-013 | El sistema debe integrarse como módulo dentro del SEACE 4.0 sin requerir autenticación independiente. | Alta | El acceso al módulo se realiza mediante la sesión institucional existente en el 100% de los casos. |
| RF-014 | El sistema debe permitir la visualización de resultados antes de la publicación del proceso o documento en el flujo correspondiente del SEACE. | Media | La visualización de alertas y resultados está disponible en el 100% de los flujos funcionales definidos. |
| RF-015 | El sistema debe registrar bitácoras de auditoría sobre análisis ejecutados, usuario, fecha, documento y resultado. | Alta | El 100% de las ejecuciones deja evidencia registrada en la bitácora del sistema. |
| RF-016 | El sistema debe permitir la consulta histórica de análisis previos asociados a documentos evaluados. | Media | La consulta histórica devuelve resultados correctamente en al menos el 95% de las búsquedas realizadas. |

## 3.2 Requerimientos No Funcionales

| ID | Categoría | Descripción | Métrica / Umbral |
|----|-----------|-------------|------------------|
| RNF-001 | Rendimiento | El tiempo de respuesta del análisis completo del documento debe ser aceptable para operación institucional. | p95 < 30 segundos por documento |
| RNF-002 | Escalabilidad | El sistema debe soportar múltiples análisis concurrentes sin degradación crítica del servicio. | Soporte mínimo de 50 análisis concurrentes |
| RNF-003 | Seguridad | El sistema debe aplicar autenticación y autorización integradas al ecosistema del SEACE. | OAuth 2.0 / JWT + control de roles |
| RNF-004 | Disponibilidad | El sistema debe estar disponible para operación institucional de forma continua. | ≥ 99.5% mensual (SLA) |
| RNF-005 | Cumplimiento | El sistema debe alinearse a la normativa aplicable sobre protección de datos y seguridad institucional. | Cumplimiento con lineamientos institucionales y normativa peruana vigente |
| RNF-006 | Observabilidad | El sistema debe registrar eventos, métricas y trazas para monitoreo y soporte. | Logs estructurados y dashboards en tiempo real |
| RNF-007 | Auditabilidad | Toda decisión, score y alerta generada por el sistema debe ser trazable. | 100% de los análisis con trazabilidad registrada |
| RNF-008 | Usabilidad | La interfaz del módulo debe ser simple e integrada al flujo del SEACE. | ≥ 90% de usuarios completa el flujo sin asistencia especializada |
| RNF-009 | Interoperabilidad | El sistema debe integrarse con servicios y fuentes institucionales mediante interfaces estándar. | APIs REST operativas con disponibilidad ≥ 95% |
| RNF-010 | Mantenibilidad | El sistema debe permitir actualizaciones evolutivas sin afectar significativamente la continuidad operativa. | Despliegues controlados sin downtime crítico |
| RNF-011 | Explicabilidad IA | Las alertas generadas deben ser explicables y justificadas al usuario. | 100% de alertas con justificación visible |
| RNF-012 | Portabilidad | La solución debe poder desplegarse en infraestructura institucional compatible con contenedores. | Despliegue soportado en entorno institucional basado en contenedores |

---

# 4. PLAN DE TRABAJO + CRONOGRAMA

## 4.1 Estructura de Desglose del Trabajo (WBS)

| Fase | Entregable | Actividades |
|------|------------|-------------|
| F1 | Documento de Alcance del Proyecto | Definición del problema, objetivo, 5W+H, alcance, delimitación y KPIs |
| F2 | Lista de Requerimientos Técnicos y Funcionales | Identificación, priorización y definición de RF y RNF con criterios medibles |
| F3 | Diseño de Arquitectura de Solución | Definición de arquitectura C4, componentes, integración SEACE y flujo técnico |
| F4 | Diseño del Modelo de Riesgo y Scoring | Definición de reglas, indicadores, ponderaciones y criterios de clasificación |
| F5 | Desarrollo del MVP | Implementación inicial del módulo IA, análisis documental y generación de resultados |
| F6 | Integración con Fuentes | Integración con SEACE, RNP y fuentes web abiertas |
| F7 | Pruebas y Validación | Ejecución de pruebas funcionales, técnicas, de rendimiento y validación del modelo |
| F8 | Piloto y Despliegue Inicial | Puesta en operación controlada, medición inicial y ajustes |

## 4.2 Cronograma

| Fase | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Semana 5 | Semana 6 | Semana 7 | Semana 8 |
|------|----------|----------|----------|----------|----------|----------|----------|----------|
| F1 – Alcance del Proyecto | X | X |  |  |  |  |  |  |
| F2 – Requerimientos |  | X | X |  |  |  |  |  |
| F3 – Arquitectura |  |  | X | X |  |  |  |  |
| F4 – Modelo de Riesgo y Scoring |  |  | X | X |  |  |  |  |
| F5 – Desarrollo MVP |  |  |  | X | X |  |  |  |
| F6 – Integración |  |  |  |  | X | X |  |  |
| F7 – Pruebas |  |  |  |  |  | X | X |  |
| F8 – Piloto y Despliegue Inicial |  |  |  |  |  |  | X | X |

## 4.3 Asignación de Roles y Responsabilidades

| Rol | Responsabilidad | Dedicación |
|-----|-----------------|-----------|
| Dirección del SEACE | Gobernanza funcional, lineamientos y validación institucional | Parcial |
| Arquitecto de Solución IA | Diseño de arquitectura, integración y definición del enfoque técnico | Alta |
| Desarrollador Backend | Implementación de APIs, lógica del módulo y orquestación de servicios | Alta |
| Desarrollador Frontend | Integración con interfaz del SEACE y visualización de resultados | Media |
| Ingeniero de Datos / Integración | Integración con fuentes institucionales y externas | Media |
| Especialista QA | Validación funcional, técnica y pruebas del sistema | Media |
| DevOps / Infraestructura | Despliegue, monitoreo y soporte de la infraestructura | Media |

## 4.4 Estimación de Esfuerzo (Horas) - Estimación real para el proyecto se realizará un MVP

| Rol | Horas estimadas |
|-----|-----------------|
| Arquitecto de Solución IA | 120 horas |
| Desarrollador Backend | 200 horas |
| Desarrollador Frontend | 120 horas |
| Ingeniero de Datos / Integración | 80 horas |
| Especialista QA | 80 horas |
| DevOps / Infraestructura | 80 horas |
| **Total estimado** | **680 horas** |

## 4.5 Estimación de Costo Operacional Mensual (Presupuesto inicial en evaluación)

| Componente | Descripción | Costo estimado mensual |
|------------|-------------|------------------------|
| Infraestructura | Plataforma de contenedores, cómputo y red | USD 1,500 – 3,000 |
| Procesamiento IA | Ejecución de modelos, inferencia y capacidad de cómputo | USD 1,000 – 2,500 |
| Almacenamiento | Base de datos, evidencias, logs y documentos asociados | USD 500 – 1,000 |
| Observabilidad | Monitoreo, dashboards, alertas y trazabilidad | USD 300 – 800 |
| **Total estimado mensual** |  | **USD 3,300 – 7,300** |

## 4.6 Selección Inicial de Tecnologías y Justificación

| Componente | Tecnología sugerida | Justificación |
|------------|---------------------|---------------|
| Backend | Spring Boot o FastAPI | Permite construir APIs robustas, mantenibles e integrables |
| Frontend | Angular | Compatible con entornos empresariales y enfoque del SEACE |
| Motor IA | LLM + RAG | Permite análisis semántico avanzado y comparación contextual |
| Base de datos | PostgreSQL | Estable, robusta y adecuada para persistencia transaccional |
| Motor de búsqueda | OpenSearch | Soporta indexación, búsqueda y análisis de documentos |
| Infraestructura | OpenShift o contenedores institucionales | Alineado a despliegues empresariales y escalabilidad |
| Seguridad | OAuth 2.0 / JWT | Facilita integración con autenticación institucional |
| Observabilidad | Logs estructurados + dashboards | Permite monitoreo, trazabilidad y soporte operativo |

---

# 5. ARQUITECTURA DE SOLUCIÓN

## 5.1 Arquitectura C4 – Contexto

El sistema se concibe como un módulo especializado dentro del ecosistema del SEACE 4.0. Interactúa con usuarios institucionales, fuentes de información internas y servicios externos relevantes para la validación de riesgos.

### Actores principales

- Usuarios institucionales del SEACE
- Dirección del SEACE – OECE
- Equipo técnico de TI / Arquitectura
- Instancias de supervisión y control

### Sistemas y fuentes relacionadas

- SEACE 4.0
- Registro Nacional de Proveedores (RNP)
- Fuentes web abiertas nacionales
- Servicios internos institucionales de autenticación, auditoría y monitoreo

## 5.2 Arquitectura C4 – Contenedores

| Contenedor | Función principal |
|------------|-------------------|
| Frontend SEACE | Interfaz integrada donde el usuario visualiza resultados, alertas e informes |
| Backend del Módulo IA | Orquesta el flujo funcional, integra servicios y gestiona la lógica del sistema |
| Motor de Análisis Documental | Extrae, limpia y estructura el contenido de los documentos cargados |
| Motor IA (RAG + LLM) | Realiza análisis semántico, contraste contextual y apoyo a la identificación de riesgos |
| Motor de Búsqueda | Consulta información indexada y apoya la recuperación de fuentes comparables |
| Motor de Scoring | Calcula el nivel de riesgo a partir de reglas, pesos e indicadores definidos |
| Base de Datos / Auditoría | Almacena resultados, evidencia, bitácoras y trazabilidad del análisis |

## 5.3 Componentes Principales del Módulo

| Componente | Descripción |
|------------|-------------|
| Agente Analizador | Identifica requisitos, condiciones y elementos relevantes del documento |
| Agente Comparador | Contrasta el documento con procesos similares y patrones de referencia |
| Agente Investigador | Consulta fuentes adicionales como RNP y web abierta nacional |
| Agente Evaluador | Aplica reglas, ponderaciones y modelo de scoring de riesgo |
| Agente Generador | Construye el informe final, alertas y evidencia de soporte |

## 5.4 Flujo de Solución

1. El usuario accede al módulo desde el SEACE 4.0.
2. El sistema recibe o procesa el documento asociado al proceso de contratación.
3. El motor documental extrae y estructura el contenido relevante.
4. Los agentes de IA analizan el documento y consultan fuentes de apoyo.
5. El motor de scoring calcula el nivel de riesgo.
6. El sistema genera alertas, evidencia y un informe final.
7. El usuario visualiza el resultado antes de continuar con el flujo correspondiente.

---

# 6. MATRIZ DE RIESGOS DEL SISTEMA

## 6.1 Riesgos técnicos

| Riesgo | Descripción | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------------|---------|-----------|
| Falsos positivos | El sistema podría marcar como riesgoso un caso que no lo es | Media | Alta | Ajuste de reglas, calibración del modelo y validación con expertos |
| Falsos negativos | El sistema podría no detectar un riesgo real presente en el documento | Media | Alta | Mejora continua del modelo y ampliación del dataset de validación |
| Baja calidad documental | Documentos escaneados o mal estructurados reducen precisión del análisis | Alta | Media | Preprocesamiento, OCR y validaciones de calidad de entrada |
| Dependencia de fuentes externas | Caídas o lentitud en fuentes integradas afectan el análisis | Media | Media | Mecanismos de caché, reintentos y degradación controlada del servicio |

## 6.2 Riesgos operativos

| Riesgo | Descripción | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------------|---------|-----------|
| Resistencia al uso | Usuarios pueden desconfiar de la herramienta basada en IA | Media | Media | Capacitación, enfoque de apoyo y explicabilidad de resultados |
| Uso indebido del resultado | Los usuarios pueden interpretar la alerta como decisión final o sanción | Media | Alta | Incluir disclaimers, manual de uso y lineamientos institucionales |
| Sobrecarga operativa | Alto volumen de análisis podría degradar el desempeño del sistema | Baja | Alta | Escalabilidad horizontal y monitoreo continuo |

## 6.3 Riesgos legales e institucionales

| Riesgo | Descripción | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------------|---------|-----------|
| Interpretación como prueba de corrupción | El resultado podría ser usado indebidamente como prueba concluyente | Media | Alta | Definir expresamente el carácter de apoyo y no decisorio del sistema |
| Observaciones de control | Falta de trazabilidad o sustento podría originar cuestionamientos institucionales | Media | Alta | Trazabilidad completa, evidencia visible y documentación técnica formal |
| Sesgo del modelo | El sistema podría priorizar patrones inadecuados por sesgo de datos o reglas | Baja | Alta | Auditoría del modelo, revisión periódica y validación con expertos |

---

# 7. MODELO DE SCORING IA

## 7.1 Enfoque general

El sistema utilizará un modelo híbrido de evaluación de riesgo que combinará reglas determinísticas, señales derivadas del análisis de mercado, comparación con procesos similares y análisis semántico basado en IA.

Este enfoque permite brindar resultados más explicables y controlables, evitando depender exclusivamente de un único tipo de algoritmo o de una sola fuente de evidencia.

## 7.2 Componentes del scoring

### Reglas determinísticas

| Indicador | Peso referencial |
|-----------|------------------|
| Mención explícita de marca | 20 |
| Mención de modelo específico | 20 |
| Ausencia de expresión equivalente o similar justificada | 15 |
| Certificación restrictiva no justificada | 15 |
| Exigencia de experiencia excesivamente específica | 10 |

### Análisis de mercado

| Indicador | Peso referencial |
|-----------|------------------|
| Número reducido de proveedores potenciales | 10 |
| Concentración del mercado aparente | 10 |
| Limitación geográfica o de distribución observable | 5 |

### Análisis comparativo con SEACE

| Indicador | Peso referencial |
|-----------|------------------|
| Divergencia significativa frente a procesos similares | 10 |
| Requisitos más restrictivos que el promedio observado | 10 |

### Análisis semántico mediante IA

| Indicador | Peso referencial |
|-----------|------------------|
| Alta similitud con ficha comercial o brochure | 15 |
| Lenguaje excesivamente alineado a producto específico | 10 |
| Justificación técnica débil o insuficiente | 10 |

## 7.3 Fórmula referencial

**Riesgo Total = Σ (Indicadores detectados × Peso asignado)**

## 7.4 Clasificación de riesgo

| Rango | Nivel |
|-------|-------|
| 0 – 30 | Bajo |
| 31 – 60 | Medio |
| 61 – 100 | Alto |

## 7.5 Ejemplo de aplicación

Si el sistema detecta una marca explícita, un modelo específico, poca pluralidad de proveedores y una alta similitud con una ficha comercial, el score acumulado podría superar el umbral de riesgo alto, generando una alerta prioritaria para revisión.

---

# 8. EXPLICABILIDAD Y USO RESPONSABLE DE LA IA

El sistema debe garantizar explicabilidad en sus resultados, permitiendo al usuario comprender por qué se generó una alerta o una clasificación determinada. Para ello, cada resultado deberá incluir fragmentos del documento analizado, reglas aplicadas, fuentes consultadas y justificación del score obtenido.

La solución tendrá carácter de apoyo y no reemplazará la evaluación humana, la interpretación jurídica ni las decisiones administrativas. Su función será proporcionar indicios, alertas y elementos de análisis para fortalecer el control preventivo dentro del proceso de contratación pública.

---

# 9. CONCLUSIONES

La implementación de un sistema de apoyo basado en Inteligencia Artificial como extensión del SEACE 4.0 representa una oportunidad relevante para fortalecer el análisis preventivo de documentos de contratación pública.

La solución propuesta permite integrar análisis documental, consulta de fuentes relevantes, evaluación de riesgo y generación de evidencia trazable dentro del flujo institucional, contribuyendo a mejorar la transparencia, la eficiencia operativa y la calidad de los procesos de contratación.

Asimismo, al definir con claridad el alcance, los requerimientos, la arquitectura, el plan de trabajo, la matriz de riesgos y el modelo de scoring, se establece una base sólida para evolucionar la propuesta hacia una futura implementación institucional.

---

# 10. ANEXO RESUMEN EJECUTIVO

## Resumen del proyecto

- **Proyecto:** Sistema de apoyo para identificación de riesgos en contrataciones públicas mediante IA  
- **Entidad:** OECE  
- **Plataforma objetivo:** SEACE 4.0  
- **Responsable funcional:** Dirección del SEACE  
- **Enfoque:** Extensión funcional integrada al SEACE  
- **Objetivo principal:** Detectar riesgos de direccionamiento con evidencia trazable  
- **Resultado esperado:** Alertas, scoring e informe de apoyo para la toma de decisiones  

## Entregables principales

1. Documento de Alcance del Proyecto
2. Lista de Requerimientos Técnicos y Funcionales
3. Plan de Trabajo + Cronograma
4. Arquitectura de Solución
5. Matriz de Riesgos
6. Modelo de Scoring IA
7. Ruta GitHub: https://github.com/brettsacuna/SAIRCP-LLM-RAG
