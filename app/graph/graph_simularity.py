import networkx as nx

def node_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    nodes1 = {data["lemma"] for data in g1.nodes(data=True)}
    nodes2 = {data["lemma"] for data in g2.nodes(data=True)}

    intersection = nodes1.intersection(nodes2)

    if len(nodes1) == 0:
        return 0
    return len(intersection) / len(nodes1)

def edge_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    edges1 = {(u, v) for u, v in g1.edges()}
    edges2 = {(u, v) for u, v in g2.edges()}

    intersection = edges1.intersection(edges2)

    if len(edges1) == 0:
        return 0
    return len(intersection) / len(edges1)

def graph_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    nodes_score = node_similarity(g1, g2)
    edges_score = edge_similarity(g1, g2)

    return 0.7 * nodes_score + 0.3 * edges_score