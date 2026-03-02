from pathlib import Path

def load_document(path: Path) -> str:
    """Load a UTF-8 text document from disk.

    Args:
        path: Path to the text file.

    Returns:
        The full document content as a string.

    """
    return path.read_text(encoding="utf-8")


def split_into_paragraph_chunks(text: str) -> list[str]:
    """Split text into paragraph-based chunks.

    This uses blank lines (double newline) as separators. It also trims
    whitespace and removes empty chunks.

    Args:
        text: Full document content.

    Returns:
        A list of paragraph chunks (non-empty).
    """
    raw_chunks = text.split("\n\n")
    chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]
    return chunks

    