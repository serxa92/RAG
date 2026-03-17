# 🤖 Local RAG Question-Answering System
<div align="center">
<p align="center">
  Local Retrieval-Augmented Generation system running fully offline
</p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/LLM-Ollama-black?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-7C3AED?style=for-the-badge)
![RAG](https://img.shields.io/badge/Architecture-RAG-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PDF](https://img.shields.io/badge/Data-PDF-orange?style=for-the-badge)

</div>


<div align="center">
  <img src="https://cdn.simpleicons.org/python" height="50" alt="Python" />
  <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" height="50" alt="Streamlit" />
  <img src="https://avatars.githubusercontent.com/u/139895814?s=200&v=4" height="50" alt="ChromaDB" />
  
</div>


This project implements a **Retrieval-Augmented Generation (RAG)** system that runs completely locally, without relying on external APIs.

The system allows users to ask questions about a set of documents (in this case, a PDF), retrieving relevant information and generating answers using a local language model.


 ⚙️ [Installation](#️installation)
 ▶️ [Usage](#️usage)
 🧠 [How it works](#how-it-works-rag-pipeline)
 ⚠️ [Notes](#️notes)



## Features

- Fully local execution (no paid APIs required)
- Semantic search using vector embeddings
- Context-aware answer generation
- CLI interface for testing
- Web interface using Streamlit



##  Tech Stack

- **Ollama** → Local LLM and embeddings (`llama3`, `nomic-embed-text`)
- **ChromaDB** → Vector database for semantic search
- **Python** → Core language
- **Streamlit** → Web interface
- **pypdf** → PDF text extraction




## Installation

### 1. Clone the repository

```bash
git clone https://github.com/serxa92/RAG
cd RAG
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

#### Activate it:

### Windows:
```bash
.venv\Scripts\activate
```

### Linux / Mac:
```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

##  4. Install Ollama

Download from:
https://ollama.com

Then install required models:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## Usage

### Step 1 — Index the documents

Processes the PDF and stores embeddings in ChromaDB.
```bash
python ingest.py
Step 2 — Query from CLI
python query.py
```

| Example:
```bash
What is object-oriented programming?
```
### Step 3 — Run web interface
```bash
python -m streamlit run app.py
```

### Open in browser:
```bash
http://localhost:8501
```

## How it works (RAG pipeline)

1. The document is split into chunks

2. Each chunk is converted into an embedding

3. Embeddings are stored in ChromaDB

4. The user question is converted into an embedding

5. The system retrieves the most similar chunks

6. The LLM generates a response using that context

---

### Notes

- You must run ingest.py before querying

- The chroma_db/ folder is generated automatically

- Do NOT upload chroma_db/ to GitHub

- Answer quality depends on chunking and retrieval

---

### Author
```bash
Sergio Agulla.
Developed as part of an internship project
```


