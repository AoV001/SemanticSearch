import spacy

"""
Text Processing Utilities

Provides basic NLP preprocessing functions using spaCy.

Functions:
- split_sentences(text): splits text into a list of sentences
- preprocess_sentence(sentence): tokenizes a sentence into lowercase lemmas,
  removing stopwords and punctuation for further analysis
"""

# load the model one time by starting the app
nlp = spacy.load("en_core_web_sm")


def split_sentences(text: str) -> list[str]:
    # split the text in sentences
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def preprocess_sentence(sentence: str) -> list[str]:
    # make the sentence as a list of lemmas
    doc = nlp(sentence)

    tockens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return tockens
