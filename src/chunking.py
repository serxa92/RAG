from pathlib import Path


def load_document(path: Path) -> str:
    """Load a UTF-8 text document from disk.

    Args:
        path: Path to the text file.

    Returns:
        The full document content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path.resolve()}")

    return path.read_text(encoding="utf-8")


def split_into_paragraph_chunks(text: str) -> list[str]:
    """Split text into paragraph-based chunks.

    This method uses blank lines (double newline) as separators.
    It trims whitespace and removes empty chunks.

    NOTE:
        This strategy works well for clean .txt or .md files,
        but may be unreliable for PDFs where formatting is inconsistent.

    Args:
        text: Full document content.

    Returns:
        A list of paragraph chunks (non-empty).
    """
    raw_chunks = text.split("\n\n")
    return [chunk.strip() for chunk in raw_chunks if chunk.strip()]


def split_into_fixed_size_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> list[str]:
    """Split text into fixed-size chunks with overlap.

    This strategy is recommended for PDF text because paragraph
    structure is often unreliable after extraction.

    The overlap ensures that important information that spans across
    chunk boundaries is not lost.

    Example:
        chunk_size = 1200
        overlap = 200

        Chunk 1: characters 0–1199
        Chunk 2: characters 1000–2199
        Chunk 3: characters 2000–3199

    Args:
        text: Full document content.
        chunk_size: Target chunk size in characters.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of non-empty text chunks.

    Raises:
        ValueError: If chunk_size or overlap values are invalid.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    # Normalize whitespace:
    # PDFs often contain strange line breaks or multiple spaces.
    # This collapses all whitespace into single spaces.
    cleaned_text = " ".join(text.split())

    chunks: list[str] = []

    start = 0
    step = chunk_size - overlap

    while start < len(cleaned_text):
        end = start + chunk_size

        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks