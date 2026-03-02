"""
Integration test for PDF ingestion + fixed-size chunking.

This script verifies that:
1. The PDF text extraction works correctly.
2. The fixed-size chunking generates a reasonable number of chunks.
3. The output chunks contain readable text.

This is not a formal unit test framework test (e.g., pytest),
but a manual integration test for development validation.
"""

from pathlib import Path

from src.pdf_ingestion import extract_text_from_pdf
from src.chunking import split_into_fixed_size_chunks


# Path to the knowledge base PDF
PDF_PATH = Path("data/programacion.pdf")


def main() -> None:
    """Run PDF ingestion and chunking validation."""

    print("Starting PDF chunking test...")

    # Extract full text from PDF
    text = extract_text_from_pdf(PDF_PATH)

    print("Total characters extracted:", len(text))

    # Basic sanity check
    if len(text) == 0:
        raise RuntimeError("No text extracted from PDF.")

    # Generate fixed-size chunks with overlap
    chunks = split_into_fixed_size_chunks(
        text,
        chunk_size=1200,
        overlap=200
    )

    print("Number of chunks generated:", len(chunks))

    if len(chunks) == 0:
        raise RuntimeError("No chunks generated.")

    # Show preview of first chunk
    print("\nFirst chunk preview (first 500 characters):\n")
    print(chunks[0][:500])


if __name__ == "__main__":
    main()