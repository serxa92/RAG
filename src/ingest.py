from pathlib import Path
import chromadb
import requests
from pypdf import PdfReader

# Path to the PDF knowledge base
PDF_PATH = Path("data/programacion.pdf")

# Local folder where Chroma will persist its database
CHROMA_PATH = "chroma_db"

# Name of the Chroma collection
COLLECTION_NAME = "programming_notes"

# Local Ollama embedding model
EMBED_MODEL = "nomic-embed-text"

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


def split_into_fixed_size_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 300
) -> list[str]:
    """Split text into fixed-size chunks with overlap.

    This is more robust for PDF text than paragraph-based chunking.

    Args:
        text: Full document text.
        chunk_size: Target chunk size in characters.
        overlap: Overlapping characters between consecutive chunks.

    Returns:
        List of text chunks.

    Raises:
        ValueError: If chunk_size or overlap are invalid.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    # Normalize whitespace to avoid broken PDF formatting issues
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


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for a given text using Ollama.

    Args:
        text: Input text.

    Returns:
        Embedding vector as a list of floats.

    Raises:
        requests.HTTPError: If Ollama returns an error.
    """
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        },
        timeout=60
    )

    response.raise_for_status()
    return response.json()["embedding"]


def create_clean_collection():
    """Create a clean Chroma collection.

    If the collection already exists, it is deleted first to avoid duplicates.

    Returns:
        A fresh Chroma collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        # Ignore if the collection does not exist yet
        pass

    return client.get_or_create_collection(name=COLLECTION_NAME)


def ingest_pdf() -> None:
    """Run the full indexing pipeline for the PDF."""
    print("Starting ingestion...")

    # 1) Extract text from PDF
    text = extract_text_from_pdf(PDF_PATH)
    print(f"Extracted characters: {len(text)}")

    # 2) Split text into chunks
    chunks = split_into_fixed_size_chunks(text, chunk_size=1200, overlap=300)
    print(f"Generated chunks: {len(chunks)}")

    # 3) Create a fresh Chroma collection
    collection = create_clean_collection()

    # 4) Embed and store each chunk
    for i, chunk in enumerate(chunks):
        chunk_id = f"chunk_{i}"

        embedding = generate_embedding(chunk)

        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": PDF_PATH.name,
                "chunk_index": i
            }]
        )

        print(f"Indexed chunk {i + 1}/{len(chunks)}")

    print("\nIngestion completed successfully.")
    print(f"Total chunks stored in Chroma: {collection.count()}")


if __name__ == "__main__":
    ingest_pdf()