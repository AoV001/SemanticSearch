import pytest
from app.services.search_service import search
from app.db.database import init_db


@pytest.fixture(autouse=True)
def setup():
    init_db()


TEXT = """
The boy kicked the ball because he was playing football.
The girl ran home after she saw him.
The dog barked loudly before it got to sleep.
"""


class TestSearch:

    def test_returns_tuple(self):
        results, resolved, coref = search(
            questions=["Who kicked the ball?"], text=TEXT, top_k=1
        )
        assert isinstance(results, dict)
        assert isinstance(resolved, str)
        assert isinstance(coref, dict)

    def test_question_in_results(self):
        results, _, _ = search(questions=["Who kicked the ball?"], text=TEXT, top_k=1)
        assert "Who kicked the ball?" in results

    def test_multiple_questions(self):
        questions = ["Who kicked the ball?", "Who ran home?"]
        results, _, _ = search(questions=questions, text=TEXT, top_k=1)
        assert len(results) == 2

    def test_answer_found_for_who(self):
        results, _, _ = search(
            questions=["Who kicked the ball?"], text=TEXT, top_k=1, threshold=0.3
        )
        hits = results.get("Who kicked the ball?", [])
        assert len(hits) > 0
        _, _, _, answer = hits[0]
        assert answer is not None
        assert "boy" in answer.lower()

    def test_high_threshold_no_results(self):
        # Вопрос который точно не совпадёт с текстом
        results, _, _ = search(
            questions=["Who invented the telephone?"],
            text=TEXT,
            top_k=1,
            threshold=0.99,
        )
        hits = results.get("Who invented the telephone?", [])
        assert len(hits) == 0

    def test_empty_text_no_results(self):
        results, _, _ = search(questions=["Who kicked the ball?"], text="", top_k=1)
        hits = results.get("Who kicked the ball?", [])
        assert len(hits) == 0

    def test_resolved_text_not_empty(self):
        _, resolved, _ = search(questions=["Who kicked the ball?"], text=TEXT, top_k=1)
        assert len(resolved) > 0

    def test_coref_map_is_dict(self):
        _, _, coref = search(questions=["Who kicked the ball?"], text=TEXT, top_k=1)
        assert isinstance(coref, dict)

    def test_result_structure(self):
        results, _, _ = search(
            questions=["Who kicked the ball?"], text=TEXT, top_k=1, threshold=0.3
        )
        hits = results.get("Who kicked the ball?", [])
        if hits:
            block, score, triplets, answer = hits[0]
            assert isinstance(block, str)
            assert 0.0 <= score <= 1.0
            assert isinstance(triplets, list)
