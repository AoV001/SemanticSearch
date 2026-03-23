from app.graph.graph_builder import build_dependency_graph
from app.graph.graph_similarity import graph_similarity
from app.nlp.text_processing import split_sentences
from app.nlp.coreference import simple_coreference
from spacy.lang.en import English
from app.graph.graph_similarity import graph_similarity, extract_relevant_subgraph


WINDOW_SIZE = 3

def split_blocks(sentences, window_size=WINDOW_SIZE):
    blocks = []
    for i in range(len(sentences) - window_size + 1):
        block = " ".join(sentences[i:i+window_size])
        blocks.append(block)
    return blocks

def search(question: str, text: str, top_k: int=3, threshold: float = 0.2):
    nlp_sent = English()
    nlp_sent.add_pipe("sentencizer")
    cleaned_text = text.replace("\n", " ")
    doc = nlp_sent(cleaned_text)

    sentences = [sent.text.strip() for sent in doc.sents]
    blocks = split_blocks(sentences, window_size=WINDOW_SIZE)

    resolved_blocks = [simple_coreference(block) for block in blocks]

    question_graph = build_dependency_graph(question)
    results = []

    for block in resolved_blocks:
        block_graph = build_dependency_graph(block)
        score = graph_similarity(question_graph, block_graph)
        if score >= threshold:
            triplets = extract_relevant_subgraph(question_graph, block_graph, hop=1)
            results.append((block, score, triplets))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]