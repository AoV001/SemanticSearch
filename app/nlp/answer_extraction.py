import spacy

nlp = spacy.load("en_core_web_sm")


QUESTION_TYPES = {
    "who":   {"deps": ["nsubj", "nsubjpass", "attr"], "ents": ["PERSON", "ORG"]},
    "when":  {"deps": ["npadvmod", "tmod", "prep"],   "ents": ["DATE", "TIME"]},
    "where": {"deps": ["prep", "npadvmod"],            "ents": ["GPE", "LOC", "FAC"]},
    "what":  {"deps": ["nsubj", "dobj", "attr"],       "ents": ["PRODUCT", "WORK_OF_ART", "ORG", "NORP"]},
    "how":   {"deps": ["advmod", "npadvmod"],          "ents": ["QUANTITY", "CARDINAL"]},
    "why":   {"deps": ["advcl", "prep"],               "ents": []},
    "which": {"deps": ["nsubj", "dobj", "attr"],       "ents": []},
}

def classify_question(question: str) -> str:
    """Определяем тип вопроса по первому слову."""
    first = question.strip().lower().split()[0]
    for qtype in QUESTION_TYPES:
        if first.startswith(qtype):
            return qtype
    return "what"  # fallback


def extract_why_answer(triplets: list, original_block: str) -> str | None:
    """Для why — ищем advcl связь и извлекаем всю причинную клаузу."""

    # Шаг 1: находим глагол причинной клаузы через advcl
    cause_verb = None
    for u, rel, v in triplets:
        if rel == "advcl":
            cause_verb = v
            break

    if not cause_verb:
        return None

    # Шаг 2: в оригинальном блоке ищем клаузу с because/since/so
    doc = nlp(original_block)

    CAUSE_MARKERS = {"because", "since", "as", "so", "therefore", "thus"}

    for token in doc:
        if token.text.lower() in CAUSE_MARKERS:
            # Берём всё предложение от маркера до точки
            clause_tokens = []
            for t in doc[token.i:]:
                if t.text in {".", "!", "?"}:
                    break
                clause_tokens.append(t.text)
            if clause_tokens:
                return " ".join(clause_tokens)

    # Fallback: собираем клаузу из triplets вокруг cause_verb
    related = []
    for u, rel, v in triplets:
        if u == cause_verb or v == cause_verb:
            related.append(f"{u} {v}")

    return " ".join(related) if related else cause_verb

def extract_answer(triplets: list, question_graph, original_block: str, original_question: str = "") -> str | None:
    # Классифицируем по оригинальному вопросу, не по леммам графа
    qtype = classify_question(original_question if original_question else "what")
    strategy = QUESTION_TYPES[qtype]

    if qtype == "why":
        result = extract_why_answer(triplets, original_block)
        return result

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