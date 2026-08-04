"""Cached vector index and retrieval operations for RAG."""

from dataclasses import dataclass
from hashlib import sha256
from threading import RLock

import numpy as np

from app.rag.chunking import split_into_chunks
from app.rag.embeddings import encode


@dataclass(frozen=True)
class RetrievedChunk:
    """A document chunk selected for answering a question."""

    text: str
    score: float


@dataclass(frozen=True)
class DocumentIndex:
    """Sentence-aligned chunks and their normalised embedding vectors."""

    chunks: tuple[str, ...]
    embeddings: np.ndarray


_indexes: dict[tuple[str, str], DocumentIndex] = {}
_index_lock = RLock()


def _cache_key(filename: str, text: str) -> tuple[str, str]:
    return filename, sha256(text.encode("utf-8")).hexdigest()


def get_or_create_index(filename: str, text: str) -> DocumentIndex:
    """Return a cached index, rebuilding it when the file contents change."""
    key = _cache_key(filename, text)
    with _index_lock:
        cached = _indexes.get(key)
        if cached is not None:
            return cached

    chunks = tuple(split_into_chunks(text))
    embeddings = encode(chunks) if chunks else np.empty((0, 0), dtype=np.float32)
    index = DocumentIndex(chunks=chunks, embeddings=embeddings)

    with _index_lock:
        # Keep only the current version of a file in memory.
        for old_key in [old_key for old_key in _indexes if old_key[0] == filename]:
            del _indexes[old_key]
        _indexes[key] = index
    return index


def retrieve(
    filename: str, text: str, question: str, top_k: int
) -> list[RetrievedChunk]:
    """Retrieve the ``top_k`` most semantically relevant document chunks."""
    if top_k < 1:
        return []

    index = get_or_create_index(filename, text)
    if not index.chunks:
        return []

    query_embedding = encode([question])[0]
    cosine_scores = index.embeddings @ query_embedding
    best_indexes = np.argsort(cosine_scores)[::-1][:top_k]
    return [
        RetrievedChunk(
            text=index.chunks[index_number],
            # Convert cosine similarity from [-1, 1] to the API's [0, 1].
            score=float((cosine_scores[index_number] + 1) / 2),
        )
        for index_number in best_indexes
    ]


def clear_indexes() -> None:
    """Clear cached document embeddings; useful for tests and maintenance."""
    with _index_lock:
        _indexes.clear()


def remove_index(filename: str) -> None:
    """Remove all cached index versions for a deleted document."""
    with _index_lock:
        for key in [key for key in _indexes if key[0] == filename]:
            del _indexes[key]
