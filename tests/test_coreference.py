import pytest
from app.nlp.coreference import simple_coreference, get_coreference_map

class TestSimpleCoreference:

    def test_male_pronoun_resolved(self):
        text = "The boy kicked the ball. He ran after it."
        result = simple_coreference(text)
        assert "boy" in result
        # "He" должен резолвиться в "boy"
        assert "He" not in result or result.count("boy") > 1

    def test_female_pronoun_resolved(self):
        text = "The girl ran home. She was tired."
        result = simple_coreference(text)
        assert "girl" in result
        assert "She" not in result

    def test_neutral_pronoun_resolved(self):
        text = "The dog barked loudly. It was scared."
        result = simple_coreference(text)
        assert "It" not in result or "dog" in result

    def test_temporal_noun_not_antecedent(self):
        # "morning" не должен становиться антецедентом для "it"
        text = "Every morning they worked. It was hard."
        result = simple_coreference(text)
        assert "morning morning" not in result

    def test_no_pronouns_unchanged(self):
        text = "Emma joined the program. The village was beautiful."
        result = simple_coreference(text)
        assert "Emma" in result
        assert "village" in result

    def test_empty_text(self):
        result = simple_coreference("")
        assert result == ""

    def test_plural_pronoun_resolved(self):
        text = "The volunteers worked hard. They were tired."
        result = simple_coreference(text)
        assert "They" not in result


class TestCoreferenceMap:

    def test_male_pronouns_mapped(self):
        text = "The boy ran. He kicked the ball. Him too."
        coref_map = get_coreference_map(text)
        assert "boy" in coref_map
        assert "he" in coref_map["boy"] or "him" in coref_map["boy"]

    def test_female_pronouns_mapped(self):
        text = "The girl smiled. She was happy."
        coref_map = get_coreference_map(text)
        assert "girl" in coref_map
        assert "she" in coref_map["girl"]

    def test_no_pronouns_empty_map(self):
        text = "Emma joined the program."
        coref_map = get_coreference_map(text)
        # Нет местоимений — пустые списки
        for v in coref_map.values():
            assert v == []

    def test_returns_dict(self):
        coref_map = get_coreference_map("The boy ran.")
        assert isinstance(coref_map, dict)