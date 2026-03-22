import networkx as nx
import spacy

nlp = spacy.load("en_core_web_sm")

def build_dependency_graph(sentence: str):
    doc = nlp(sentence)

    G = nx.Graph()

    for token in doc:
        G.add_node(token.text, lemma=token.lemma_.lower(), pos=token.pos_)

        if token.head != token:
            G.add_edge(token.text, token.head.text, relation=token.dep_)

    return G