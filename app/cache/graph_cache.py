from app.graph.graph_builder import build_dependency_graph

_cache: dict = {}

def get_graph(text: str):
    if text not in _cache:
        _cache[text] = build_dependency_graph(text)
    return _cache[text]

def clear_cache():
    _cache.clear()

def cache_size() -> int:
    return len(_cache)