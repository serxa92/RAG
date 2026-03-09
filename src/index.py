from pathlib import Path

import chromadb
import requests

from src.pdf_ingestion import extract_text_from_pdf
from src.chunking import split_into_fixed_size_chunks


# Path to the PDF knowledge base
PDF_PATH = Path("data/programacion.pdf")

# Directory where Chroma will persist its data locally
CHROMA_PATH = "chroma_db"

# Name of the collection inside Chroma
COLLECTION_NAME = "programming_notes"

# Embedding model served locally by Ollama
EMBED_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for a given text using Ollama.

    Args:
        text: Input text to embed.

    Returns:
        A numeric vector representing the semantic meaning of the text.

    Raises:
        requests.HTTPError: If Ollama returns an unsuccessful response.
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


def get_or_create_collection():
    """Create or load a persistent Chroma collection.

    Returns:
        A Chroma collection object stored locally on disk.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def index_pdf() -> None:
    """Extract text from PDF, split it into chunks and store them in Chroma.
     This function:
    1. Extracts text from the PDF.
    2. Splits the text into fixed-size chunks.
    3. Generates an embedding for each chunk.
    4. Stores chunk text + embedding + metadata in ChromaDB."""
    
    print("Starting indexing process...")

    # 1. Extract full text from PDF
    text = extract_text_from_pdf(PDF_PATH)
    print(f"Extracted characters: {len(text)}")

    # 2. Split text into chunks
    chunks = split_into_fixed_size_chunks(text, chunk_size=1200, overlap=200)
    print(f"Generated chunks: {len(chunks)}")

    # 3. Load or create Chroma collection
    collection = get_or_create_collection()

    # Clear previous data to avoid duplicates during development
    existing_count = collection.count()
    if existing_count > 0:
        print(f"Collection already contains {existing_count} items.")
        print("Adding new chunks may create duplicates if you run this multiple times.")

    # 4. Process every chunk and store it
    for i, chunk in enumerate(chunks):
         # Unique identifier for the chunk
        chunk_id = f"chunk_{i}"

        embedding = generate_embedding(chunk)
        
        # Store:
        # - id: unique key
        # - document: original chunk text
        # - embedding: numeric vector used for similarity search
        # - metadata: extra information to trace the source
        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": str(PDF_PATH.name),
                "chunk_index": i
            }]
        )

        print(f"Indexed chunk {i + 1}/{len(chunks)}")

    print("\nIndexing completed successfully.")
    print(f"Total chunks stored in Chroma: {collection.count()}")


if __name__ == "__main__":
    index_pdf()