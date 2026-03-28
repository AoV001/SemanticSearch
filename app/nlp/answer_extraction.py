import spacy

nlp = spacy.load("en_core_web_sm")


QUESTION_TYPES = {
    "who":   {"deps": ["nsubj", "nsubjpass", "attr"], "ents": ["PERSON", "ORG"]},
    "when":  {"deps": ["npadvmod", "tmod", "prep"],   "ents": ["DATE", "TIME"]},
    "where": {"deps": ["prep", "npadvmod", "pobj"],   "ents": ["GPE", "LOC", "FAC"]},
    "what":  {"deps": ["dobj", "attr", "nsubj"],      "ents": ["PRODUCT", "WORK_OF_ART", "ORG", "NORP"]},
    "how":   {"deps": ["advmod", "npadvmod", "acomp", "xcomp"], "ents": ["QUANTITY", "CARDINAL"]},
    "why":   {"deps": ["advcl", "prep"],               "ents": []},
    "which": {"deps": ["nsubj", "dobj", "attr"],       "ents": []},
}

def classify_question(question: str) -> str:

    first = question.strip().lower().split()[0]
    for qtype in QUESTION_TYPES:
        if first.startswith(qtype):
            return qtype
    return "what"  # fallback


def extract_why_answer(triplets: list, original_block: str) -> str | None:

    cause_verb = None
    for u, rel, v in triplets:
        if rel == "advcl":
            cause_verb = v
            break

    if not cause_verb:
        return None


    doc = nlp(original_block)

    CAUSE_MARKERS = {"because", "since", "as", "so", "therefore", "thus"}

    for token in doc:
        if token.text.lower() in CAUSE_MARKERS:

            clause_tokens = []
            for t in doc[token.i:]:
                if t.text in {".", "!", "?"}:
                    break
                clause_tokens.append(t.text)
            if clause_tokens:
                return " ".join(clause_tokens)


    related = []
    for u, rel, v in triplets:
        if u == cause_verb or v == cause_verb:
            related.append(f"{u} {v}")

    return " ".join(related) if related else cause_verb



def extract_answer(triplets: list, question_graph, original_block: str, original_question: str = "") -> str | None:
    qtype = classify_question(original_question if original_question else "what")
    strategy = QUESTION_TYPES[qtype]

    if qtype == "why":
        return extract_why_answer_v2(original_block)

    if qtype == "where":
        return extract_where_answer(triplets, original_block)

    if qtype == "what":
        return extract_what_answer(triplets, original_block, question_graph)

    if qtype == "how":
        return extract_how_answer(triplets, original_block)

    target_deps = strategy["deps"]
    for u, rel, v in triplets:
        if rel in target_deps:
            if rel in {"nsubj", "nsubjpass"}:
                return u
            else:
                return v

    target_ents = strategy["ents"]
    if target_ents:
        doc = nlp(original_block)
        for ent in doc.ents:
            if ent.label_ in target_ents:
                return ent.text

    return None


def extract_where_answer(triplets, original_block: str) -> str | None:
    """Для where — ищем GPE/LOC entity или pobj от prep."""
    doc = nlp(original_block)

    # Сначала NER
    for ent in doc.ents:
        if ent.label_ in {"GPE", "LOC", "FAC"}:
            return ent.text

    # Потом pobj — объект предлога
    for u, rel, v in triplets:
        if rel == "pobj":
            return v
        if rel == "prep":
            # ищем pobj от этого предлога в тексте
            for token in doc:
                if token.text == v and token.dep_ == "prep":
                    for child in token.children:
                        if child.dep_ == "pobj":
                            return child.text

    return None


def extract_what_answer(triplets, original_block: str, question_graph) -> str | None:
    question_verbs = {
        data["lemma"] for _, data in question_graph.nodes(data=True)
        if data.get("pos") == "VERB"
    }

    # 1. dobj от глагола вопроса
    for u, rel, v in triplets:
        if rel == "dobj" and u.lower() in question_verbs:
            return v

    # 2. любой dobj
    for u, rel, v in triplets:
        if rel == "dobj":
            return v

    # 3. amod где v это существительное из вопроса или ключевое слово
    question_nouns = {
        data["lemma"] for _, data in question_graph.nodes(data=True)
        if data.get("pos") in {"NOUN", "PROPN"}
    }
    for u, rel, v in triplets:
        if rel == "amod" and (v.lower() in question_nouns or u.lower() in question_nouns):
            return v

    # 4. глагол из npadvmod — "what did they do" → берём сам глагол
    for u, rel, v in triplets:
        if rel == "npadvmod":
            return v  # v это глагол действия

    # 5. attr
    for u, rel, v in triplets:
        if rel == "attr":
            return v

    # 6. nsubj от organized/happened — для "what happened"
    q_lower = " ".join(question_verbs)
    if any(w in q_lower for w in {"happen", "occur", "take"}):
        for u, rel, v in triplets:
            if rel == "nsubj":
                return u

    # NER fallback
    doc = nlp(original_block)
    for ent in doc.ents:
        if ent.label_ in {"PRODUCT", "WORK_OF_ART", "ORG", "NORP", "FAC", "EVENT"}:
            return ent.text

    return None


def extract_how_answer(triplets, original_block: str) -> str | None:
    # acomp — прилагательное после feel/seem/become
    for u, rel, v in triplets:
        if rel == "acomp":
            return v

    # advmod
    for u, rel, v in triplets:
        if rel == "advmod":
            return v

    # xcomp — только если это не глагол
    doc = nlp(original_block)
    for u, rel, v in triplets:
        if rel == "xcomp":
            for token in doc:
                if token.text == v and token.pos_ == "ADJ":
                    return v

    # Fallback — прилагательное после copula
    COPULA_VERBS = {"feel", "become", "seem", "look", "sound", "appear", "get"}
    for token in doc:
        if token.lemma_.lower() in COPULA_VERBS:
            for child in token.children:
                if child.dep_ in {"acomp", "advmod"} and child.pos_ in {"ADJ", "ADV"}:
                    return child.text

    return None


def extract_why_answer_v2(original_block: str) -> str | None:
    doc = nlp(original_block)
    # "because" и "since" — настоящие причинные маркеры
    # "as" только если НЕ часть "such as"
    CAUSE_MARKERS = {"because", "since", "therefore", "thus"}

    for sent in doc.sents:
        for token in sent:
            t = token.text.lower()
            if t in CAUSE_MARKERS:
                clause = [x.text for x in sent if x.i >= token.i and x.text not in {".", "!", "?"}]
                if clause:
                    return " ".join(clause)
            # "as" только если предыдущий токен не "such"
            if t == "as":
                prev = doc[token.i - 1] if token.i > 0 else None
                if prev and prev.text.lower() != "such":
                    clause = [x.text for x in sent if x.i >= token.i and x.text not in {".", "!", "?"}]
                    if clause:
                        return " ".join(clause)

    return None


DEP_LABELS = {
    "nsubj":    lambda u, v: f"{u} performs '{v}'",
    "nsubjpass":lambda u, v: f"{u} is subject of '{v}'",
    "dobj":     lambda u, v: f"'{u}' acts on {v}",
    "advcl":    lambda u, v: f"'{u}' happens because/when '{v}'",
    "prep":     lambda u, v: f"'{u}' is related to '{v}'",
    "attr":     lambda u, v: f"'{u}' is described as '{v}'",
    "advmod":   lambda u, v: f"'{v}' describes how '{u}' happens",
    "npadvmod": lambda u, v: f"'{v}' tells when/how '{u}'",
    "tmod":     lambda u, v: f"'{u}' happens at '{v}'",
    "amod":     lambda u, v: f"'{v}' describes '{u}'",
    "pobj":     lambda u, v: f"object of preposition: '{v}'",
    "iobj":     lambda u, v: f"'{u}' is given/shown to '{v}'",
    "conj":     lambda u, v: f"'{u}' and '{v}' are connected",
    "relcl":    lambda u, v: f"'{v}' describes '{u}'",
    "acl":      lambda u, v: f"'{v}' describes '{u}'",
    "ccomp":    lambda u, v: f"'{u}' implies that '{v}'",
    "xcomp":    lambda u, v: f"'{u}' leads to '{v}'",
    "aux":      lambda u, v: f"helper verb '{v}' for '{u}'",
    "neg":      lambda u, v: f"'{u}' is negated",
    "compound": lambda u, v: f"'{u} {v}' is a compound",
    "poss":     lambda u, v: f"'{v}' belongs to '{u}'",
}

def format_triplets(triplets: list[tuple]) -> list[str]:

    result = []
    for u, rel, v in triplets:
        formatter = DEP_LABELS.get(rel)
        if formatter:
            result.append(formatter(u, v))
        else:
            result.append(f"'{u}' → '{v}' ({rel})")
    return result

# answer_extraction.py — заменяем всю temporal часть

TEMPORAL_MARKERS = {"before", "after", "when", "while", "then"}
SEQUENTIAL_MARKERS = {"as soon as"}  # двусловные — обрабатываем отдельно
QUANTITATIVE_MARKERS = {"how long", "how often", "how much", "how many"}

# Какую клаузу брать для каждого маркера
# "same" = всё предложение, "before" = до маркера, "after" = после маркера
MARKER_STRATEGY = {
    # маркер в тексте → что брать если вопрос спрашивает before/after/while
    "after":      {"before": "after",  "after": "before", "while": "same"},
    "before":     {"before": "before", "after": "after",  "while": "same"},
    "while":      {"while": "after",   "before": "before","after": "after"},
    "then":       {"after": "after",   "before": "before","then": "after"},
    "as soon as": {"after": "after",   "before": "before","as soon as": "after"},
    "when":       {"when": "after",    "before": "before","after": "after"},
}

def _get_clause(sent, token_i: int, side: str) -> str | None:
    """Извлекаем клаузу до или после позиции token_i в предложении."""
    if side == "before":
        tokens = [t.text for t in sent if t.i < token_i and not t.is_punct]
    elif side == "after":
        tokens = [t.text for t in sent if t.i > token_i and not t.is_punct]
    else:  # same — всё предложение
        tokens = [t.text for t in sent if not t.is_punct]
    return " ".join(tokens) if tokens else None

def _get_anchor_words(question: str, marker: str) -> set:
    """Слова после маркера в вопросе — используем как якорь для поиска предложения."""
    words = question.lower().split()
    marker_words = marker.split()
    # ищем позицию маркера в вопросе
    for i in range(len(words)):
        if words[i:i+len(marker_words)] == marker_words:
            anchor = set(words[i + len(marker_words):])
            anchor -= {"the", "a", "an", "to", "?", "did", "was", "is", "do", "does"}
            return anchor
    return set()

def extract_temporal_answer(original_block: str, original_question: str) -> str | None:
    q_lower = original_question.lower()
    words = q_lower.split()

    # Определяем маркер вопроса (сначала двусловные)
    q_marker = None
    for m in SEQUENTIAL_MARKERS:
        if m in q_lower:
            q_marker = m
            break
    if not q_marker:
        for m in TEMPORAL_MARKERS:
            if m in words:
                q_marker = m
                break

    # Проверяем quantitative
    for qm in QUANTITATIVE_MARKERS:
        if q_lower.startswith(qm):
            return extract_quantitative_answer(original_block, original_question)

    if not q_marker:
        return None

    anchor_words = _get_anchor_words(original_question, q_marker)
    doc = nlp(original_block)

    for sent in doc.sents:
        sent_lemmas = {t.lemma_.lower() for t in sent}

        # Предложение должно содержать хотя бы одно слово из якоря
        if anchor_words and not sent_lemmas & anchor_words:
            continue

        sent_text = sent.text.lower()

        # Ищем маркер в предложении (сначала двусловные)
        for text_marker, strategies in MARKER_STRATEGY.items():
            if text_marker not in sent_text:
                continue
            side = strategies.get(q_marker)
            if not side:
                continue

            # Находим позицию маркера в предложении
            marker_words = text_marker.split()
            for token in sent:
                if token.text.lower() == marker_words[0]:
                    # Для двусловных проверяем следующий токен
                    if len(marker_words) > 1:
                        next_tok = sent[token.i + 1] if token.i + 1 < len(sent) else None
                        if not next_tok or next_tok.text.lower() != marker_words[1]:
                            continue
                    result = _get_clause(sent, token.i, side)
                    if result:
                        return result

    return None


def extract_quantitative_answer(original_block: str, original_question: str) -> str | None:
    """Для how long/often/much/many — ищем NUMBER/DATE/QUANTITY entity."""
    q_lower = original_question.lower()
    anchor_words = set(q_lower.split()) - {
        "how", "long", "often", "much", "many", "did",
        "does", "was", "the", "a", "an", "?"
    }

    doc = nlp(original_block)
    TARGET_ENTS = {"DATE", "TIME", "QUANTITY", "CARDINAL", "PERCENT", "MONEY"}

    for sent in doc.sents:
        sent_lemmas = {t.lemma_.lower() for t in sent}
        if not sent_lemmas & anchor_words:
            continue
        for ent in sent.ents:
            if ent.label_ in TARGET_ENTS:
                return ent.text

    # Fallback — ищем числа через POS
    for sent in doc.sents:
        sent_lemmas = {t.lemma_.lower() for t in sent}
        if not sent_lemmas & anchor_words:
            continue
        for token in sent:
            if token.pos_ == "NUM":
                # берём число + следующее слово для контекста ("2 hours", "every day")
                next_tok = sent[token.i + 1] if token.i + 1 < len(sent) else None
                if next_tok and next_tok.pos_ in {"NOUN", "ADV"}:
                    return f"{token.text} {next_tok.text}"
                return token.text

    return None