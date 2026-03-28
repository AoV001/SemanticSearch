from app.graph.graph_builder import build_dependency_graph
from app.nlp.coreference import simple_coreference


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

def clear_cache():
    _cache.clear()

def cache_size() -> int:
    return len(_cache)