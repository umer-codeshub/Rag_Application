"""Turn files (disk or upload) into plain text. Raises RAGError with friendly messages."""
import hashlib
import io
from pathlib import Path

from pypdf import PdfReader

from errors import RAGError

SUPPORTED_EXTENSIONS = (".txt", ".md", ".pdf")


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _decode(data: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RAGError("Could not decode the text file.")


def _read_pdf(data: bytes, filename: str) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            raise RAGError(f"'{filename}' is password-protected and cannot be read.")
        pages = [(page.extract_text() or "") for page in reader.pages]
    except RAGError:
        raise
    except Exception:
        raise RAGError(f"Could not read '{filename}'. The PDF may be corrupted.")
    return "\n\n".join(pages)


def extract_text(filename: str, data: bytes) -> str:
    """Return raw text from a TXT, MD or PDF file's bytes."""
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise RAGError(f"Unsupported file type '{extension}'. Use TXT, MD or PDF.")
    if not data:
        raise RAGError(f"'{filename}' is empty.")

    text = _read_pdf(data, filename) if extension == ".pdf" else _decode(data)

    if not text.strip():
        hint = " It may be a scanned PDF (images only), which needs OCR." if extension == ".pdf" else ""
        raise RAGError(f"No text could be extracted from '{filename}'.{hint}")
    return text


def read_folder(folder) -> list[tuple[str, bytes]]:
    """Read all supported files from a folder as (filename, bytes)."""
    folder = Path(folder)
    if not folder.is_dir():
        raise RAGError(f"Knowledge base folder not found: {folder}")
    files = [p for p in sorted(folder.iterdir()) if p.suffix.lower() in SUPPORTED_EXTENSIONS]
    if not files:
        raise RAGError(f"No TXT, MD or PDF files found in {folder}")
    return [(p.name, p.read_bytes()) for p in files]