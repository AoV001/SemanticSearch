from app.graph.graph_builder import build_dependency_graph, nlp
from app.nlp.coreference import simple_coreference

"""
NLP Processing Cache

Provides simple in-memory caching for expensive NLP operations used in the
search pipeline. The module caches results of coreference resolution,
dependency graph construction, and spaCy document parsing to avoid
recomputing them for the same input text.

Functions:
- get_resolved(text): returns cached coreference-resolved text
- get_graph(text): returns cached dependency graph
- get_doc(text): returns cached spaCy Doc object
- clear_cache(): clears the graph cache
- cache_size(): returns the current size of the graph cache
"""

_doc_cache: dict = {}
_coref_cache: dict = {}
_cache: dict = {}


def get_resolved(text: str) -> str:
    if text not in _coref_cache:
        _coref_cache[text] = simple_coreference(text)
    return _coref_cache[text]


def get_graph(text: str):
    if text not in _cache:
        _cache[text] = build_dependency_graph(text)
    return _cache[text]


def get_doc(text: str):
    if text not in _doc_cache:
        _doc_cache[text] = nlp(text)
    return _doc_cache[text]


def clear_cache():
    _cache.clear()


def cache_size() -> int:
    return len(_cache)
