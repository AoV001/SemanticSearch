from unittest.mock import Mock, patch

import numpy as np

from app.rag.generator import clear_answer_cache, generate_answer
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


def test_generated_answer_is_cached():
    clear_answer_cache()
    response = Mock()
    response.json.return_value = {"message": {"content": "The boy."}}
    with patch("app.rag.generator.requests.post", return_value=response) as post:
        assert generate_answer("Who?", ["The boy kicked the ball."]) == "The boy."
        assert generate_answer("Who?", ["The boy kicked the ball."]) == "The boy."

    post.assert_called_once()


def test_rag_search_uses_vector_ranking():
    with patch(
        "app.services.search_service.retrieve",
        return_value=[Mock(text="The boy kicked the ball.", score=0.9)],
    ), patch("app.services.search_service.generate_answer", return_value="The boy."):
        results, _, _ = search(
            questions=["Who kicked the ball?"],
            text="The boy kicked the ball.",
            mode="rag",
            include_metadata=True,
        )

    assert results["Who kicked the ball?"][0][1] == 0.9
    assert results["Who kicked the ball?"][0][3] == "The boy."
    assert results["Who kicked the ball?"][0][4] == "RAG LLM"


def test_graph_rag_uses_graph_context_for_generation():
    with patch("app.services.search_service.graph_similarity", return_value=0.5), patch(
        "app.services.search_service.generate_answer", return_value="The boy."
    ) as generate_answer:
        results, _, _ = search(
            questions=["Who kicked the ball?"],
            text="The boy kicked the ball. He watched.",
            mode="graph_rag",
            threshold=0.3,
            include_metadata=True,
        )

    assert results["Who kicked the ball?"][0][3] == "The boy."
    assert "He watched." in results["Who kicked the ball?"][0][0]
    assert generate_answer.call_args.args[1][0].startswith("The boy kicked the ball.")
    assert results["Who kicked the ball?"][0][4] == "GraphRAG LLM"
    assert results["Who kicked the ball?"][0][5] is True


def test_graph_rag_skips_llm_for_confident_graph_hit():
    with patch(
        "app.services.search_service.extract_answer", return_value="The boy."
    ), patch("app.services.search_service.generate_answer") as generate_answer:
        results, _, _ = search(
            questions=["Who kicked the ball?"],
            text="The boy kicked the ball.",
            mode="graph_rag",
            threshold=0.3,
        )

    generate_answer.assert_not_called()
    assert "boy" in results["Who kicked the ball?"][0][3].lower()
