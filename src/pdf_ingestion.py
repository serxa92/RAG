from __future__ import annotations

from pathlib import Path
from pypdf import PdfReader

# Path to the PDF file.
PDF_PATH = Path("data/programacion.pdf")

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string (pages concatenated).

    Raises:
        FileNotFoundError: If the PDF does not exist.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path.resolve()}")

    reader = PdfReader(str(pdf_path))

    # Extract text from each page. Some PDFs may return None for certain pages.
    pages_text: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        pages_text.append(page_text)

    # Join pages with separators to preserve some structure
    return "\n\n".join(pages_text)


def main() -> None:
    """Run a quick ingestion check and print a text preview."""
    text = extract_text_from_pdf(PDF_PATH)

    print(f"PDF: {PDF_PATH.name}")
    print(f"Extracted characters: {len(text)}")

    preview = text[:1000].replace("\n", " ")
    print("\nPreview (first 1000 chars):")
    print(preview)


if __name__ == "__main__":
    main()