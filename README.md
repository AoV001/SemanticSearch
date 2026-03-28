# Semantic Search Engine
### Graph-Based Semantic Question Answering over Text

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![spaCy](https://img.shields.io/badge/spaCy-3.8-09A3D5?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker)

A full-stack NLP application that enables semantic question answering over user-provided texts. Unlike keyword-based search, this system analyzes the grammatical and semantic structure of both the query and the text to find meaningful answers.

---

## How It Works

The system processes input text by splitting it into overlapping sentence windows and applying a custom coreference resolution pipeline that replaces pronouns with their referents. Each window is then converted into a **dependency graph** using spaCy, where nodes represent content words and edges represent syntactic relations such as subject, object, and adverbial modifier.

When a user submits a question, the system builds a corresponding dependency graph and computes similarity scores against all text window graphs using a recall-oriented node and edge overlap metric. The top-scoring windows are selected as candidate contexts, and a **question-type-aware extraction module** then identifies the specific answer span — distinguishing between *who*, *what*, *where*, *when*, *why*, and *how* questions using different dependency patterns and named entity recognition.

---

## Features

- **Semantic search** based on dependency graph matching — no keyword overlap required
- **Coreference resolution** — pronouns are automatically resolved to their referents
- **Question-type classification** — different extraction strategies for who / what / where / when / why / how
- **Context highlighting** — hover over an answer to highlight the source sentence in the text
- **Word-level highlighting** — answer and its coreferent pronouns highlighted separately
- **Dependency graph visualization** — interactive SVG graph with hover-to-reveal relation labels
- **Dictionary lookup** — click any word in the text to see its definition via Free Dictionary API
- **Search history** — all queries stored per file in SQLite
- **File management** — upload .txt and .pdf files or paste text directly
- **Dark mode UI** — teal and pink accent colors on dark background
- **Fully containerized** — Docker + Docker Compose for both backend and frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| NLP | spaCy (`en_core_web_sm`), NetworkX |
| Database | SQLite |
| Frontend | React 18, Tailwind CSS, Vite |
| Containerization | Docker, Docker Compose |
| PDF parsing | pdfplumber |
| Dictionary API | Free Dictionary API |

---

## Architecture

```
SemanticSearch/
├── app/
│   ├── api/              # FastAPI routers (upload, search, history)
│   ├── cache/            # In-memory graph cache
│   ├── db/               # SQLite connection and history operations
│   ├── graph/            # Dependency graph builder and similarity
│   ├── nlp/              # Coreference, text processing, answer extraction
│   ├── services/         # Search orchestration, file service
│   └── main.py
├── frontend/
│   └── src/
│       ├── api/          # API client + dictionary lookup
│       ├── components/   # FileUpload, FileList, SearchForm, TextViewer,
│       │                 # ResultCard, ResultModal, HistoryOverlay, WordModal
│       └── pages/        # Home page layout
├── data/                 # Uploaded files + SQLite database
├── Dockerfile            # Backend image
├── docker-compose.yml
└── requirements.txt
```

---

## Getting Started

### With Docker (recommended)

```bash
git clone https://github.com/AoV001/semantic-search
cd semantic-search
docker-compose up --build
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:5173](http://localhost:5173)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Local development

```bash
# Backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
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
| `POST` | `/api/upload` | Upload a .txt or .pdf file |
| `POST` | `/api/upload-text` | Save pasted text as a file |
| `GET` | `/api/files` | List all uploaded files |
| `GET` | `/api/files/{filename}/text` | Get file contents |
| `DELETE` | `/api/files/{filename}` | Delete a file and its history |
| `DELETE` | `/api/files` | Delete all files |
| `POST` | `/api/search` | Run semantic search with questions |
| `GET` | `/api/history` | Get full search history |
| `GET` | `/api/history/{filename}` | Get history for a specific file |
| `DELETE` | `/api/history` | Clear all history |

---

## Key Engineering Decisions

**Sliding window with coreference** allows the system to handle cross-sentence references without external ML models. Each window of 3 sentences is resolved independently, giving the graph enough context to replace pronouns correctly.

**Asymmetric similarity metric** measures how well the text covers the question rather than symmetric overlap — which improves recall for short factual questions against longer text windows.

**Modular extraction pipeline** — question classification drives a separate extraction function for each question type, allowing targeted improvements without affecting other types. For example, *why* questions search for causal markers like *because* and *since* directly in the text, while *where* questions prioritize named entity recognition before falling back to prepositional object extraction.

**Graph caching** — dependency graphs are cached in memory after first computation, so repeated questions against the same text do not trigger reprocessing.

---

## Benchmarking and Complexity

Performance (10 questions, ~1500 char text):
- Cold start: ~2.4s (includes spaCy model loading)
- Warm (cached): ~1.3s
- Peak RAM: ~6.4 MB
- Algorithm complexity: O(B × Q × (V + E))
  where B = blocks, Q = questions, V = nodes, E = edges per graph
---

## Limitations and Future Work

The current system relies entirely on rule-based coreference resolution and syntactic matching, which limits performance on questions requiring paraphrase understanding or world knowledge. The most impactful improvements would be:

- Adding **sentence embeddings** (e.g. `sentence-transformers`) as a complementary retrieval layer alongside the graph matcher
- Extending coreference resolution to support **longer documents** with more complex reference chains
- **Multilingual support** via spaCy's multilingual models

---

## Author

**Tony V.** — [github.com/AoV001](https://github.com/AoV001)

---

*Built with Python, FastAPI, spaCy, NetworkX, and React.*
