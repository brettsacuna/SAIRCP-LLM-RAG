# SAIRCP — Ejemplos para Demo

## 1. Ejemplo para "Analizar documento" (Riesgo ALTO)

**Tipo:** TDR  
**ID Proceso:** SEACE-2026-045789  
**Entidad:** Gobierno Regional de Arequipa  

**Contenido:**
```
TÉRMINOS DE REFERENCIA
Adquisición de Equipos de Videovigilancia para Seguridad Ciudadana

1. OBJETO DE LA CONTRATACIÓN
Adquisición de un sistema de videovigilancia integral compuesto por 50 cámaras IP marca Hikvision modelo DS-2CD2T47G2-L con resolución 4MP ColorVu, grabador NVR Hikvision DS-7732NI-K4/16P de 32 canales, y software de gestión HikCentral Professional.

2. REQUISITOS TÉCNICOS
- Cámaras IP tipo bullet con tecnología ColorVu de Hikvision
- Sensor CMOS progresivo 1/1.8" de 4 Megapíxeles
- Lente focal fija de 4mm con apertura F1.0
- Iluminación LED de luz blanca con alcance de 60 metros
- Clasificación de protección IP67 e IK10
- Grabador NVR de 32 canales con 4 bahías SATA de hasta 10TB cada una
- Software de gestión centralizada con reconocimiento facial

3. EXPERIENCIA DEL POSTOR
El postor debe acreditar ser distribuidor autorizado de Hikvision en Perú con certificación HCSA (Hikvision Certified Security Associate) vigente. Experiencia mínima de 8 años en proyectos de videovigilancia en el sector público con un monto acumulado no menor a 5 veces el valor referencial.

4. GARANTÍA Y SOPORTE
Garantía de fábrica Hikvision de 3 años. Soporte técnico 24/7 con tiempo de respuesta no mayor a 4 horas. Centro de servicio autorizado Hikvision en la región.

5. PLAZO DE ENTREGA
Cuarenta y cinco (45) días calendario.
```

---

## 2. Ejemplo para "Analizar documento" (Riesgo BAJO)

**Tipo:** ESPECIFICACIONES_TECNICAS  
**ID Proceso:** SEACE-2026-078123  
**Entidad:** Municipalidad Provincial de Trujillo  

**Contenido:**
```
ESPECIFICACIONES TÉCNICAS
Adquisición de Mobiliario de Oficina para la Sede Central

1. OBJETO
Adquisición de mobiliario de oficina ergonómico para equipar 30 puestos de trabajo administrativo.

2. ESPECIFICACIONES
2.1. Escritorios (30 unidades)
- Tipo: Escritorio en L con superficie de melamina de 25mm de espesor o similar
- Dimensiones mínimas: 1.50m x 1.50m x 0.75m de altura
- Estructura metálica con acabado en pintura electrostática o equivalente
- Color: a definir por la entidad
- Con pasacables integrado

2.2. Sillas ergonómicas (30 unidades)
- Tipo: Silla giratoria con regulación de altura
- Asiento y respaldo tapizado en tela mesh o equivalente
- Soporte lumbar ajustable
- Apoyabrazos regulables en altura
- Base de 5 ruedas con freno automático
- Capacidad mínima: 120 kg
- Certificación de ergonomía según norma técnica vigente o equivalente

3. EXPERIENCIA
Experiencia en venta de mobiliario de oficina al sector público o privado por un monto acumulado no menor al 50% del valor referencial en los últimos 3 años.

4. GARANTÍA
Garantía mínima de 2 años contra defectos de fabricación.

5. PLAZO
Veinte (20) días calendario desde la firma del contrato.
```

---

## 3. Ejemplo para "Consulta RAG"

### Pregunta 1:
```
¿Cuáles son los indicadores de riesgo más comunes en TDR de equipos tecnológicos?
```

### Pregunta 2:
```
¿Qué dice la normativa peruana sobre mencionar marcas específicas en documentos de contratación pública?
```

### Pregunta 3:
```
¿Cuál es la diferencia entre riesgo MEDIO y riesgo ALTO en el sistema de scoring del SAIRCP?
```

---

## 4. Ejemplo para "Ingesta"

```json
[
  {
    "id": "SEACE-2025-REF-001",
    "content": "Adquisición de 20 laptops para trabajo remoto del personal administrativo. Se requiere laptops con procesador Intel Core i7 de 12va generación o AMD Ryzen 7 serie 6000 o equivalente, 16GB RAM DDR5, SSD NVMe 512GB, pantalla 14 pulgadas FHD IPS. Sistema operativo Windows 11 Pro licenciado. El postor debe tener experiencia mínima de 2 años en venta de equipos de cómputo. Garantía mínima de 3 años del fabricante. Plazo de entrega: 15 días calendario.",
    "metadata": {
      "entity": "OECE",
      "year": 2025,
      "type": "TDR",
      "object": "Laptops para trabajo remoto",
      "risk_level": "BAJO",
      "amount": 180000
    }
  },
  {
    "id": "SEACE-2025-REF-002",
    "content": "Contratación del servicio de cloud computing para la plataforma digital institucional. Se requiere infraestructura en nube pública con certificación SOC 2 Type II e ISO 27001. Mínimo 3 años de experiencia del proveedor en servicios cloud para el sector público latinoamericano. Disponibilidad garantizada de 99.95%. Data center en la región de Sudamérica. Soporte técnico 24/7 en español. Migración asistida de los sistemas actuales.",
    "metadata": {
      "entity": "Ministerio de Economía",
      "year": 2025,
      "type": "TDR",
      "object": "Servicio cloud computing",
      "risk_level": "MEDIO",
      "amount": 450000
    }
  },
  {
    "id": "SEACE-2025-REF-003",
    "content": "Adquisición de servidores para el Data Center. Se requieren 10 servidores rack 2U con procesador de al menos 32 cores, 256GB RAM DDR5 ECC, almacenamiento 4x 1.92TB SSD NVMe en RAID 10, doble fuente de poder redundante 800W, interfaces de red 2x 10GbE y 2x 1GbE. Compatible con VMware vSphere 8 o equivalente. El proveedor debe contar con certificación del fabricante y experiencia de 3 años en proyectos similares.",
    "metadata": {
      "entity": "RENIEC",
      "year": 2025,
      "type": "ESPECIFICACIONES_TECNICAS",
      "object": "Servidores Data Center",
      "risk_level": "BAJO",
      "amount": 850000
    }
  }
]
```

---

## 5. Flujo de demo sugerido para el video

1. **Abrir** http://localhost:3000 → mostrar dashboard vacío
2. **Ingestar** los 3 documentos de referencia (sección 4)
3. **Analizar** el TDR de videovigilancia (riesgo ALTO) → mostrar score, alertas, evidencia
4. **Analizar** el TDR de mobiliario (riesgo BAJO) → comparar resultado
5. **Consulta RAG** con las 3 preguntas → mostrar respuestas con fuentes
6. **Dashboard** → mostrar estadísticas actualizadas
7. **Estado** → verificar health check con todos los componentes verdes
