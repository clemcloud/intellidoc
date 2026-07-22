from pypdf import PdfReader
from docx import Document
import os


def extract_text(file_path: str) -> str:
    # figure out what kind of file we're dealing with from the extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext == ".docx":
        return _extract_docx(file_path)

    raise ValueError(f"can't handle this file type yet: {ext}")


def _extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            pages.append(content)

    text = "\n".join(pages).strip()

    # scanned/image-only PDFs won't give us any text here
    # we'd need OCR for those, not doing that for now
    if not text:
        raise ValueError("no text found in this PDF, might be a scanned document")

    return text


def _extract_docx(file_path: str) -> str:
    doc = Document(file_path)

    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs).strip()

    if not text:
        raise ValueError("no text found in this docx")

    return text