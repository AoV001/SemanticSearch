import networkx as nx


def node_similarity(g1, g2):
    # g1 = вопрос, g2 = блок
    nodes1 = {data.get("lemma") for _, data in g1.nodes(data=True) if "lemma" in data}
    nodes2 = {data.get("lemma") for _, data in g2.nodes(data=True) if "lemma" in data}

    intersection = nodes1 & nodes2
    if not nodes1:
        return 0
    # Recall: сколько узлов вопроса нашлось в блоке
    return len(intersection) / len(nodes1)


def edge_similarity(g1, g2):
    def edge_set(g):
        lemmas = {n: d.get("lemma") for n, d in g.nodes(data=True)}
        return {
            tuple(sorted([lemmas[u], lemmas[v]]))
            for u, v in g.edges()
            if lemmas.get(u) and lemmas.get(v)
        }

    edges1, edges2 = edge_set(g1), edge_set(g2)
    if not edges1:
        return 0
    # Тоже recall по рёбрам вопроса
    return len(edges1 & edges2) / len(edges1)

def graph_similarity(g1: nx.DiGraph, g2: nx.DiGraph):

    nodes_score = node_similarity(g1, g2)
    edges_score = edge_similarity(g1, g2)

    return 0.7 * nodes_score + 0.3 * edges_score


def extract_relevant_subgraph(question_graph, block_graph, hop=1):
    question_lemmas = {
        data["lemma"]
        for _, data in question_graph.nodes(data=True)
        if "lemma" in data
    }

    seed_nodes = {
        node for node, data in block_graph.nodes(data=True)
        if data.get("lemma") in question_lemmas
    }

    # Расширяем БЕЗ фильтра по вопросу — берём всех соседей seed
    relevant_nodes = set(seed_nodes)
    for _ in range(hop):
        neighbors = set()
        for node in list(relevant_nodes):
            if node in block_graph:
                neighbors.update(block_graph.neighbors(node))
        relevant_nodes.update(neighbors)

    triplets = []
    for u, v, data in block_graph.edges(data=True):
        if u in relevant_nodes and v in relevant_nodes:
            triplets.append((u, data.get("relation", "?"), v))

    return triplets


