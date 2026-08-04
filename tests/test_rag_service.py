from unittest.mock import Mock, patch

import numpy as np

from app.rag.retriever import clear_indexes, retrieve
from app.services.search_service import search


def test_retrieve_returns_normalized_scores():
    clear_indexes()
    model = Mock()
    model.encode.side_effect = [
        np.array([[1.0, 0.0], [0.0, 1.0]]),
        np.array([[1.0, 0.0]]),
    ]

    with patch("app.rag.embeddings.get_embedding_model", return_value=model):
        ranked = retrieve(
            "file.txt",
            "Relevant sentence. One more sentence. Third sentence. Other sentence.",
            "question",
            2,
        )

    assert [item.score for item in ranked] == [1.0, 0.5]


def test_rag_search_uses_vector_ranking():
    with patch(
        "app.services.search_service.retrieve",
        return_value=[Mock(text="The boy kicked the ball.", score=0.9)],
    ), patch("app.services.search_service.generate_answer", return_value="The boy."):
        results, _, _ = search(
            questions=["Who kicked the ball?"],
            text="The boy kicked the ball.",
            mode="rag",
        )

    assert results["Who kicked the ball?"][0][1] == 0.9
    assert results["Who kicked the ball?"][0][3] == "The boy."


def test_graph_rag_uses_graph_context_for_generation():
    with patch(
        "app.services.search_service.generate_answer", return_value="The boy."
    ) as generate_answer:
        results, _, _ = search(
            questions=["Who kicked the ball?"],
            text="The boy kicked the ball. The girl watched.",
            mode="graph_rag",
            threshold=0.3,
        )

    assert results["Who kicked the ball?"][0][3] == "The boy."
    assert generate_answer.call_args.args[1][0].startswith("The boy kicked the ball.")
