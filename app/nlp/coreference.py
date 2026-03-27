import spacy

nlp = spacy.load("en_core_web_sm")

FIRST_PERSON = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
SECOND_PERSON = {"you", "your", "yours"}
MALE = {"he", "him", "his"}
FEMALE = {"she", "her", "hers"}
NEUTRAL = {"it", "its"}
PLURAL = {"they", "them", "their", "theirs"}
PRONOUNS = FIRST_PERSON | SECOND_PERSON | MALE | FEMALE | NEUTRAL | PLURAL

# semantic sets for gender
MALE_NOUNS = {
    "boy", "man", "father", "son", "brother", "uncle", "king", "prince",
    "husband", "grandfather", "guy", "male", "sir", "mr", "lord"
}
FEMALE_NOUNS = {
    "girl", "woman", "mother", "daughter", "sister", "aunt", "queen",
    "princess", "wife", "grandmother", "lady", "female", "mrs", "ms", "madam"
}

def get_gender(token) -> str | None:

    lower = token.lemma_.lower()
    if lower in MALE_NOUNS:
        return "Masc"
    if lower in FEMALE_NOUNS:
        return "Fem"
    # for inanimate always neutral
    if token.ent_type_ in {"PERSON", "ORG"}:
        return "Neut"
    return None

def simple_coreference(text: str) -> str:
    doc = nlp(text)

    last = {
        "Masc": None,
        "Fem": None,
        "Neut": None,
        "Plur": None,
    }

    resolved_tokens = []

    for token in doc:
        lower = token.text.lower()


        if token.pos_ in {"NOUN", "PROPN"} and lower not in PRONOUNS:
            gender = get_gender(token)
            if gender == "Masc":
                last["Masc"] = token.text
            elif gender == "Fem":
                last["Fem"] = token.text
            elif gender == "Neut":
                last["Neut"] = token.text
            else:

                last["Neut"] = token.text
            resolved_tokens.append(token.text)
            continue

        # Резолвим местоимения
        if lower in MALE and last["Masc"]:
            resolved_tokens.append(last["Masc"])
        elif lower in FEMALE and last["Fem"]:
            resolved_tokens.append(last["Fem"])
        elif lower in NEUTRAL and last["Neut"]:
            resolved_tokens.append(last["Neut"])
        elif lower in PLURAL:
            # they/them — берём последнее существительное любого рода
            candidate = last["Plur"] or last["Masc"] or last["Fem"] or last["Neut"]
            resolved_tokens.append(candidate if candidate else token.text)
        else:
            resolved_tokens.append(token.text)

    return _rebuild_text(resolved_tokens)


def _rebuild_text(tokens: list[str]) -> str:
    """Собираем токены обратно в строку с пробелами."""
    result = ""
    for tok in tokens:
        if tok in {".", ",", "?", "!", ":", ";", "'s"}:
            result += tok
        else:
            if result and result[-1] not in {" ", "\n"}:
                result += " "
            result += tok
    return result.strip()


def get_coreference_map(text: str) -> dict:
    doc = nlp(text)

    last = {"Masc": None, "Fem": None, "Neut": None, "Plur": None}
    coref_map = {}  # noun -> set of pronouns

    for token in doc:
        lower = token.text.lower()

        if token.pos_ in {"NOUN", "PROPN"} and lower not in PRONOUNS:
            gender = get_gender(token)
            noun = token.text
            if noun not in coref_map:
                coref_map[noun] = set()
            if gender == "Masc":
                last["Masc"] = noun
            elif gender == "Fem":
                last["Fem"] = noun
            else:
                last["Neut"] = noun
            continue

        if lower in MALE and last["Masc"]:
            coref_map.setdefault(last["Masc"], set()).add(lower)
        elif lower in FEMALE and last["Fem"]:
            coref_map.setdefault(last["Fem"], set()).add(lower)
        elif lower in NEUTRAL and last["Neut"]:
            coref_map.setdefault(last["Neut"], set()).add(lower)
        elif lower in PLURAL:
            candidate = last["Plur"] or last["Masc"] or last["Fem"] or last["Neut"]
            if candidate:
                coref_map.setdefault(candidate, set()).add(lower)

    return {k: list(v) for k, v in coref_map.items()}