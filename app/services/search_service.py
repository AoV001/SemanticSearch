from app.graph.graph_builder import build_dependency_graph
from app.graph.graph_similarity import graph_similarity
from app.nlp.text_processing import split_sentences

def search(question: str, text: str, top_k: int=3, threshold: float = 0.2):

    sentences = split_sentences(text)

    question_graph = build_dependency_graph(question)

    results = []

    for sentence in sentences:

        s_graph = build_dependency_graph(sentence)
        score = graph_similarity(question_graph, s_graph)
        if score >= threshold:
            results.append((sentence, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]