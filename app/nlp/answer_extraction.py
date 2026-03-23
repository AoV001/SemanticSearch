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
    """Переводим технические triplets в читаемые фразы."""
    result = []
    for u, rel, v in triplets:
        formatter = DEP_LABELS.get(rel)
        if formatter:
            result.append(formatter(u, v))
        else:
            result.append(f"'{u}' → '{v}' ({rel})")
    return result