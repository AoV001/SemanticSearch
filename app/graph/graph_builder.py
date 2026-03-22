import networkx as nx
import spacy

nlp = spacy.load("en_core_web_sm")

def build_dependency_graph(sentence: str):
    doc = nlp(sentence)

    G = nx.Graph()

    for token in doc:

        if token.is_punct or token.is_stop:
            continue

        G.add_node(
            token.text,
            lemma=token.lemma_.lower(),
            pos=token.pos_
        )

    for token in doc:

        if token.is_punct or token.is_stop:
            continue

        head = token.head

        if head != token and not head.is_punct and not head.is_stop:
            G.add_edge(
                head.text,
                token.text,
                relation=token.dep_
            )
    return G