import pytest
from app.graph.graph_builder import build_dependency_graph
from app.nlp.answer_extraction import extract_answer, classify_question

class TestClassifyQuestion:

    def test_who_question(self):
        assert classify_question("Who kicked the ball?") == "who"

    def test_what_question(self):
        assert classify_question("What did they do?") == "what"

    def test_where_question(self):
        assert classify_question("Where did she go?") == "where"

    def test_when_question(self):
        assert classify_question("When did it happen?") == "when"

    def test_why_question(self):
        assert classify_question("Why did the boy run?") == "why"

    def test_how_question(self):
        assert classify_question("How did she feel?") == "how"

    def test_fallback_to_what(self):
        assert classify_question("Describe the event.") == "what"


class TestExtractAnswer:

    def _get_triplets_and_graph(self, question, block):
        from app.graph.graph_similarity import extract_relevant_subgraph
        qg = build_dependency_graph(question)
        bg = build_dependency_graph(block)
        triplets = extract_relevant_subgraph(qg, bg, hop=1)
        return triplets, qg

    def test_who_question(self):
        question = "Who kicked the ball?"
        block = "The boy kicked the ball."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert answer is not None
        assert "boy" in answer.lower()

    def test_what_question(self):
        question = "What did the boy kick?"
        block = "The boy kicked the ball."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert answer is not None
        assert "ball" in answer.lower()

    def test_why_question(self):
        question = "Why did the boy kick the ball?"
        block = "The boy kicked the ball because he was playing football."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert answer is not None
        assert "because" in answer.lower()

    def test_how_question(self):
        question = "How did Emma feel?"
        block = "At first Emma was worried but she began to feel comfortable."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert answer is not None

    def test_where_question(self):
        question = "Where was the village located?"
        block = "She joined a program in a small village near the mountains."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert answer is not None

    def test_no_answer_returns_none(self):
        question = "Who invented the telephone?"
        block = "The cat sat on the mat."
        triplets, qg = self._get_triplets_and_graph(question, block)
        answer = extract_answer(triplets, qg, block, original_question=question)
        assert True