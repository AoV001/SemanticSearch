import networkx as nx
from app.graph.graph_builder import build_dependency_graph
from app.graph.graph_similarity import graph_similarity, extract_relevant_subgraph


class TestBuildDependencyGraph:

    def test_returns_networkx_graph(self):
        G = build_dependency_graph("The boy kicked the ball.")
        assert isinstance(G, nx.Graph)

    def test_nodes_have_lemma(self):
        G = build_dependency_graph("The boy kicked the ball.")
        for _, data in G.nodes(data=True):
            assert "lemma" in data

    def test_nodes_have_pos(self):
        G = build_dependency_graph("The boy kicked the ball.")
        for _, data in G.nodes(data=True):
            assert "pos" in data

    def test_stopwords_filtered(self):
        G = build_dependency_graph("The boy kicked the ball.")
        node_texts = list(G.nodes())
        assert "the" not in [n.lower() for n in node_texts]
        assert "The" not in node_texts

    def test_empty_string(self):
        G = build_dependency_graph("")
        assert len(G.nodes()) == 0

    def test_edges_have_relation(self):
        G = build_dependency_graph("The boy kicked the ball.")
        for u, v, data in G.edges(data=True):
            assert "relation" in data

    def test_meta_words_filtered(self):
        G = build_dependency_graph("What is described in the text?")
        lemmas = {data["lemma"] for _, data in G.nodes(data=True)}
        assert "describe" not in lemmas
        assert "text" not in lemmas


class TestGraphSimilarity:

    def test_identical_sentences_score_one(self):
        G = build_dependency_graph("The boy kicked the ball.")
        score = graph_similarity(G, G)
        assert score == 1.0

    def test_unrelated_sentences_low_score(self):
        G1 = build_dependency_graph("The boy kicked the ball.")
        G2 = build_dependency_graph("The cat sat on the mat.")
        score = graph_similarity(G1, G2)
        assert score < 0.3

    def test_similar_sentences_high_score(self):
        G1 = build_dependency_graph("Who kicked the ball?")
        G2 = build_dependency_graph("The boy kicked the ball because he was playing.")
        score = graph_similarity(G1, G2)
        assert score > 0.4

    def test_score_between_zero_and_one(self):
        G1 = build_dependency_graph("What did Emma do?")
        G2 = build_dependency_graph("Emma joined the program.")
        score = graph_similarity(G1, G2)
        assert 0.0 <= score <= 1.0

    def test_empty_graph_returns_zero(self):
        G1 = build_dependency_graph("")
        G2 = build_dependency_graph("The boy kicked the ball.")
        score = graph_similarity(G1, G2)
        assert score == 0.0


class TestExtractRelevantSubgraph:

    def test_returns_list(self):
        G1 = build_dependency_graph("Who kicked the ball?")
        G2 = build_dependency_graph("The boy kicked the ball.")
        triplets = extract_relevant_subgraph(G1, G2, hop=1)
        assert isinstance(triplets, list)

    def test_triplets_have_three_elements(self):
        G1 = build_dependency_graph("Who kicked the ball?")
        G2 = build_dependency_graph("The boy kicked the ball.")
        triplets = extract_relevant_subgraph(G1, G2, hop=1)
        for triplet in triplets:
            assert len(triplet) == 3

    def test_relevant_nodes_present(self):
        G1 = build_dependency_graph("Who kicked the ball?")
        G2 = build_dependency_graph("The boy kicked the ball.")
        triplets = extract_relevant_subgraph(G1, G2, hop=1)
        nodes = {u for u, _, _ in triplets} | {v for _, _, v in triplets}
        assert any("kicked" in n.lower() or "ball" in n.lower() for n in nodes)
