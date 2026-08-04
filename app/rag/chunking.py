"""Text chunking utilities for vector retrieval."""

from spacy.lang.en import English


CHUNK_SIZE = 3
CHUNK_OVERLAP = 1


def split_into_chunks(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """Split text into overlapping, sentence-aligned chunks.

    Chunks stay small enough for precise retrieval while the overlap preserves
    facts whose subject and object occur in neighbouring sentences.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    sentencizer = English()
    sentencizer.add_pipe("sentencizer")
    sentences = [sentence.text.strip() for sentence in sentencizer(text).sents]
    sentences = [sentence for sentence in sentences if sentence]
    if not sentences:
        return []

    step = chunk_size - overlap
    return [
        " ".join(sentences[start : start + chunk_size])
        for start in range(0, len(sentences), step)
    ]
