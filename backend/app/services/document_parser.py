from __future__ import annotations

from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentParserError(RuntimeError):
    pass


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_text(file_path)
    if suffix == ".docx":
        return _extract_docx_text(file_path)
    raise DocumentParserError(f"Unsupported file type: {suffix}")


def _extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text_parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            text_parts.append(text.strip())
    extracted = "\n\n".join(text_parts).strip()
    if not extracted:
        raise DocumentParserError("Could not extract readable text from the PDF.")
    return extracted


def _extract_docx_text(file_path: Path) -> str:
    document = Document(str(file_path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    extracted = "\n".join(paragraphs).strip()
    if not extracted:
        raise DocumentParserError("Could not extract readable text from the DOCX file.")
    return extracted
