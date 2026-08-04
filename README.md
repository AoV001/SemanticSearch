# Semantic Search Engine
### Graph, Vector RAG, and GraphRAG Question Answering over Text

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker)

A full-stack NLP application for answering questions over uploaded text and PDF files. It offers a fast graph search, vector RAG, and a hybrid GraphRAG mode.

---

## Search Modes

| Mode | How it works | Best for |
|---|---|---|
| **Graph search** | Matches dependency graphs and extracts an answer from the strongest source fragment. | Fast factual questions with explicit wording in the document. |
| **RAG (vector search)** | Retrieves semantically similar chunks with sentence embeddings, then uses a local Ollama model to answer only from those chunks. | Paraphrased questions or weaker graph matches. |
| **Hybrid (GraphRAG)** | Runs graph search first. The LLM is called only when the best graph result is below 90% confidence or cannot produce an answer. | A balance between speed and coverage. |

Text is split into overlapping sentence windows. Graph modes resolve coreferences and build dependency graphs with spaCy. RAG retrieves sentence-aligned chunks using embeddings. In GraphRAG, at most two graph-selected source fragments are passed to the LLM. The UI displays the source context and labels every answer as graph extraction, RAG LLM, or GraphRAG LLM.

---

## Features

- Three search modes: graph, vector RAG, and confidence-gated GraphRAG
- Dependency-graph semantic matching without requiring keyword overlap
- Coreference resolution for pronouns in graph modes
- Question-type-aware extraction for who, what, where, when, why, and how questions
- Grounded local generation through Ollama, limited to retrieved contexts
- Answer provenance and source-context highlighting
- Interactive dependency-graph visualization and dictionary lookup
- Upload `.txt` and `.pdf` files or paste text directly
- Per-file search history in SQLite
- Docker Compose setup for backend and frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| NLP and graph search | spaCy (`en_core_web_sm`), NetworkX |
| RAG | sentence-transformers, NumPy, Ollama (`qwen3:4b-instruct` by default) |
| Database | SQLite |
| Frontend | React 18, Tailwind CSS, Vite |
| Containerization | Docker, Docker Compose |
| PDF parsing | pdfplumber |

---

## Architecture

```text
SemanticSearch/
├── app/
│   ├── api/          # FastAPI routers
│   ├── cache/        # In-memory graph/coreference cache
│   ├── graph/        # Dependency graph builder and similarity
│   ├── nlp/          # Coreference and answer extraction
│   ├── rag/          # Chunking, embeddings, retrieval, Ollama generation
│   ├── services/     # Search orchestration and file operations
│   └── main.py
├── frontend/src/     # React UI
├── data/             # Uploaded files and SQLite database
├── docker-compose.yml
└── requirements.txt
```

---

## Getting Started

### With Docker

```bash
git clone https://github.com/AoV001/SemanticSearch.git
cd SemanticSearch
docker compose up --build
```

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Ollama for RAG and GraphRAG

Graph-only search works without an LLM. RAG and GraphRAG require [Ollama](https://ollama.com/) running on the host machine and the configured model:

```bash
ollama pull qwen3:4b-instruct
```

Docker uses `http://host.docker.internal:11434` to reach Ollama. Change `OLLAMA_BASE_URL` or `OLLAMA_MODEL` in `docker-compose.yml` if your setup differs.

### Local Development

```bash
# Backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload` | Upload a `.txt` or `.pdf` file |
| `POST` | `/api/upload-text` | Save pasted text as a file |
| `GET` | `/api/files` | List uploaded files |
| `GET` | `/api/files/{filename}/text` | Get file contents |
| `DELETE` | `/api/files/{filename}` | Delete a file and its history |
| `POST` | `/api/search` | Run graph, RAG, or GraphRAG search |
| `GET` | `/api/history` | Get search history |

---

## Performance and Caching

Dependency graphs, resolved text, document vector indexes, question embeddings, and generated answers are cached in memory while the backend is running. This makes repeated requests faster.

The first RAG request is still slower than graph search because it must perform vector retrieval and may run a local LLM. Actual timing depends on document size, CPU/GPU, the selected Ollama model, and whether the requested answer is already cached.

Graph-search complexity is `O(B x Q x (V + E))`, where `B` is the number of text blocks, `Q` is the number of questions, and `V`/`E` are the nodes and edges in a graph.

---

## Limitations and Future Work

- Rule-based coreference resolution can be weak on long or complex documents.
- Local LLM generation is slower than graph extraction, especially on CPU.
- The current NLP pipeline is focused on English text.
- Backend progress streaming would make RAG-stage progress more precise.

---

## Author

**Tony V.** - [github.com/AoV001](https://github.com/AoV001)
