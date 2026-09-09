from io import BytesIO
from docx import Document
from pypdf import PdfReader


def extract_text(file_bytes: bytes, filename: str) -> str:
    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if extension == "docx":
        document = Document(BytesIO(file_bytes))
        paragraphs = [p.text for p in document.paragraphs]
        return "\n".join(p for p in paragraphs if p.strip())

    raise ValueError("Unsupported file type. Use PDF or DOCX.")
