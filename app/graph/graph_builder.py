import networkx as nx
import spacy

"""
Dependency Graph Builder

Creates a dependency graph from a sentence using spaCy parsing.
Each node represents a meaningful token, and edges represent
syntactic dependency relations between tokens.

The graph filters out punctuation, stopwords, and predefined
meta words to keep only semantically relevant terms.
Uses NetworkX for graph representation.
"""

nlp = spacy.load("en_core_web_sm")
META_WORDS = {
    "describe", "mention", "discuss", "say", "state", "text",
    "passage", "article", "paragraph", "author", "write", "explain"
}

def build_dependency_graph(sentence: str):
    doc = nlp(sentence)
    G = nx.Graph()

    for token in doc:
        if token.is_punct or token.is_stop:
            continue
        if token.lemma_.lower() in META_WORDS:  # фильтруем мета-слова
            continue
        G.add_node(
            token.text,
            lemma=token.lemma_.lower(),
            pos=token.pos_
        )

    for token in doc:
        if token.is_punct or token.is_stop:
            continue
        if token.lemma_.lower() in META_WORDS:
            continue
        head = token.head
        if head != token and not head.is_punct and not head.is_stop:
            if head.lemma_.lower() not in META_WORDS:
                G.add_edge(
                    head.text,
                    token.text,
                    relation=token.dep_
                )
    return G