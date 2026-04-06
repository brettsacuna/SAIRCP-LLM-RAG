"""
Agente Analizador: Extrae requisitos técnicos, comerciales,
documentales y detecta restricciones potenciales del documento.
"""

import json
from openai import AsyncOpenAI

SYSTEM_PROMPT = """Eres un analista experto en contrataciones públicas del Perú (Ley 30225 y su Reglamento).
Tu tarea es analizar documentos de contratación (TDR, bases administrativas, especificaciones técnicas, estudios de mercado) y extraer información estructurada.

DEBES RETORNAR SOLO JSON VÁLIDO con esta estructura exacta:
{
  "requirements": ["lista de requisitos técnicos, comerciales y documentales identificados"],
  "restrictions": ["lista de posibles restricciones a la competencia detectadas"],
  "brands_mentioned": ["marcas o modelos específicos mencionados"],
  "certifications": ["certificaciones exigidas"],
  "experience_requirements": ["requisitos de experiencia"],
  "geographic_restrictions": ["restricciones geográficas detectadas"],
  "equivalent_expression_present": true/false,
  "technical_justification_quality": "fuerte|débil|ausente",
  "key_fragments": [{"text": "fragmento relevante", "reason": "por qué es relevante"}]
}

RESTRICCIONES:
- Analiza SOLO en base al contenido proporcionado.
- No inventes información que no esté en el documento.
- Sé preciso en la extracción de fragmentos textuales.
- Identifica lenguaje que pueda estar alineado a fichas comerciales específicas.
"""


class AnalyzerAgent:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def extract(self, content: str, document_type: str) -> dict:
        """Extrae requisitos y restricciones del documento."""
        user_prompt = (
            f"Analiza el siguiente documento de tipo '{document_type}' "
            f"de contratación pública peruana:\n\n"
            f"---DOCUMENTO---\n{content[:12000]}\n---FIN DOCUMENTO---\n\n"
            f"Extrae toda la información estructurada según las instrucciones."
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "requirements": [],
                "restrictions": [],
                "brands_mentioned": [],
                "certifications": [],
                "experience_requirements": [],
                "geographic_restrictions": [],
                "equivalent_expression_present": False,
                "technical_justification_quality": "ausente",
                "key_fragments": [],
            }
