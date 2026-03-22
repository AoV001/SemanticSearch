import networkx as nx

def node_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    nodes1 = {data.get("lemma") for _, data in g1.nodes(data=True) if "lemma" in data}
    nodes2 = {data.get("lemma") for _, data in g2.nodes(data=True) if "lemma" in data}

    intersection = nodes1.intersection(nodes2)

    if len(nodes1) == 0:
        return 0
    return len(intersection) / len(nodes1)

def edge_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    edges1 = {
        (g1.nodes[u].get("lemma"), g1.nodes[v].get("lemma"))
        for u, v in g1.edges()
        if "lemma" in g1.nodes[u] and "lemma" in g1.nodes[v]
    }

    edges2 = {
        (g2.nodes[u].get("lemma"), g2.nodes[v].get("lemma"))
        for u, v in g2.edges()
        if "lemma" in g2.nodes[u] and "lemma" in g2.nodes[v]
    }


    intersection = edges1.intersection(edges2)

    if len(edges1) == 0:
        return 0
    return len(intersection) / len(edges1)

def graph_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    nodes_score = node_similarity(g1, g2)
    edges_score = edge_similarity(g1, g2)

    return 0.7 * nodes_score + 0.3 * edges_score