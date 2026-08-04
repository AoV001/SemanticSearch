"""Sentence-transformer embedding model used by the RAG retriever."""

from functools import lru_cache
from typing import Sequence

import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load and cache the embedding model on the first RAG request."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def encode(texts: Sequence[str]) -> np.ndarray:
    """Encode text as L2-normalised vectors for cosine-similarity search."""
    return get_embedding_model().encode(
        list(texts),
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
