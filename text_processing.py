"""Pure text functions: cleaning and chunking. No ML dependencies, easy to unit test."""
import re
import unicodedata


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_title(text: str, fallback: str) -> str:
    """Use the first markdown heading as the title, else the fallback (file name)."""
    for line in text.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return fallback


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks, preferring paragraph/sentence/word boundaries."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    chunks, start, n = [], 0, len(text)

    while start < n:
        end = min(start + chunk_size, n)
        if end < n:
            window = text[start:end]
            for sep in ["\n\n", "\n", ". ", " "]:
                pos = window.rfind(sep)
                if pos > chunk_size * 0.5:
                    end = start + pos + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break

        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = end
        while next_start < end and not text[next_start - 1].isspace():
            next_start += 1
        start = next_start

    return chunks


def build_chunks(doc_name: str, text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[dict]:
    """Section-aware chunking. Each chunk is prefixed with [Title > Section] so it keeps its context."""
    title = get_title(text, doc_name)
    records, index = [], 0
    for section in re.split(r"\n(?=## )", text):
        section = section.strip()
        if not section:
            continue
        first_line = section.splitlines()[0]
        heading = first_line.lstrip("#").strip() if first_line.startswith("#") else ""
        label = f"[{title} > {heading}]" if heading and heading != title else f"[{title}]"
        for piece in chunk_text(section, chunk_size, chunk_overlap):
            records.append({
                "doc_name": doc_name,
                "title": title,
                "chunk_index": index,
                "text": f"{label}\n{piece}",
            })
            index += 1
    return records
