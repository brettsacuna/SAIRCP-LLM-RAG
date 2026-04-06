"""Extracción de texto de documentos PDF y DOCX."""

import io


def extract_text(content_bytes: bytes, content_type: str) -> str:
    """Extrae texto de un archivo PDF o DOCX."""
    if content_type == "application/pdf":
        return _extract_pdf(content_bytes)
    elif "wordprocessingml" in content_type:
        return _extract_docx(content_bytes)
    raise ValueError(f"Tipo no soportado: {content_type}")


def _extract_pdf(data: bytes) -> str:
    try:
        import pymupdf
        doc = pymupdf.open(stream=data, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    except ImportError:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_docx(data: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
