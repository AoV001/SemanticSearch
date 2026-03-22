import spacy

nlp = spacy.load("en_core_web_sm")

FIRST_PERSON = {"i", "me", "my", "mine", "we", "us", "our", "ours"}

SECOND_PERSON = {"you", "your", "yours"}

MALE = {"he", "him", "his"}

FEMALE = {"she", "her", "hers"}

NEUTRAL = {"it", "they", "them", "its", "theirs"}

PRONOUNS = FIRST_PERSON | SECOND_PERSON | MALE | FEMALE | NEUTRAL

def simple_coreference(text: str):

    doc = nlp(text)

    last = {
        "Masc": None,
        "Fem": None,
        "Neut": None
    }

    resolved_tokens = []

    for token in doc:

        lower = token.text.lower()
        gender = token.morph.get("Gender")
        if gender:
            gender = gender[0]  # spaCy возвращает список

        # Существительные, не местоимения
        if token.pos_ in {"NOUN"} and lower not in PRONOUNS:
            if gender == "Masc":
                last["Masc"] = token.text
            elif gender == "Fem":
                last["Fem"] = token.text
            else:
                last["Neut"] = token.text
            resolved_tokens.append(token.text)
            continue

        if lower in MALE and last["Masc"]:
            resolved_tokens.append(last["Masc"])
        elif lower in FEMALE and last["Fem"]:
            resolved_tokens.append(last["Fem"])
        elif lower in NEUTRAL and last["Neut"]:
            resolved_tokens.append(last["Neut"])
        else:
            resolved_tokens.append(token.text)


    resolved_text = ""
    for tok in resolved_tokens:
        if tok in {".", ",", "?", "!"}:
            resolved_text += tok
            if tok == ".":
                resolved_text += " "
        else:
            if resolved_text and resolved_text[-1] not in {" ", "\n", "."}:
                resolved_text += " "
            resolved_text += tok

    return resolved_text