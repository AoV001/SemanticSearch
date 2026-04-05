from spacy.lang.en import English
from app.graph.graph_similarity import graph_similarity, extract_relevant_subgraph
from app.nlp.answer_extraction import (
    extract_answer,
    extract_temporal_answer,
    TEMPORAL_MARKERS,
)
from app.cache.graph_cache import get_graph
from app.nlp.coreference import simple_coreference, get_coreference_map
from typing import List
from app.db.history import save_search
from app.cache.graph_cache import get_resolved

"""
Search Service

Handles the main search pipeline: splitting text, resolving coreferences,
building graphs, comparing with question graphs, extracting answers, and
recording search history.

Key Functions:
- split_blocks(sentences, window_size): groups sentences into overlapping blocks
- search(questions, text, top_k, threshold, filename):
    - resolves coreferences in blocks
    - builds dependency graphs for questions and blocks
    - computes graph similarity
    - extracts answers (including temporal questions)
    - stores results and top answers in history
    - returns: (all_results, resolved_text, coref_map)

Constants:
- WINDOW_SIZE: number of sentences per block
- ALL_TEMPORAL: set of temporal markers for identifying temporal questions
"""

WINDOW_SIZE = 3
ALL_TEMPORAL = TEMPORAL_MARKERS | {
    "as soon as",
    "how long",
    "how often",
    "how much",
    "how many",
}

TEMPORAL_QUESTION_WORDS = {"before", "after", "when", "while"}


def split_blocks(sentences, window_size=WINDOW_SIZE):
    blocks = []
    for i in range(len(sentences) - window_size + 1):
        block = " ".join(sentences[i : i + window_size])
        blocks.append(block)
    return blocks


def search(
    questions: List[str], text: str, top_k: int = 3, threshold=0.3, filename: str = ""
):
    nlp_sent = English()
    nlp_sent.add_pipe("sentencizer")
    cleaned_text = text.replace("\n", " ")
    doc = nlp_sent(cleaned_text)

    sentences = [sent.text.strip() for sent in doc.sents]
    blocks = split_blocks(sentences, window_size=WINDOW_SIZE)
    resolved_blocks = [get_resolved(block) for block in blocks]
    coref_map = get_coreference_map(" ".join(sentences))

    resolved_sentences = []

    for i, sent in enumerate(sentences):

        context = sentences[i - 1] + " " + sent if i > 0 else sent
        resolved = simple_coreference(context)

        if i > 0:
            prev_resolved = simple_coreference(sentences[i - 1])
            resolved = resolved[len(prev_resolved) :].strip()
        resolved_sentences.append(resolved)

    resolved_text = " ".join(resolved_sentences)
    all_results = {}

    for question in questions:
        question_graph = get_graph(question)
        results = []

        for block in resolved_blocks:
            block_graph = get_graph(block)
            score = graph_similarity(question_graph, block_graph)
            if score >= threshold:
                triplets = extract_relevant_subgraph(question_graph, block_graph, hop=1)
                answer = extract_answer(
                    triplets, question_graph, block, original_question=question
                )
                is_temporal = any(m in question.lower() for m in ALL_TEMPORAL)
                if is_temporal:
                    temporal = extract_temporal_answer(block, question)
                    if temporal:
                        answer = temporal
                results.append((block, score, triplets, answer))

        results.sort(key=lambda x: x[1], reverse=True)
        all_results[question] = results[:top_k]

        best = all_results[question][0] if all_results[question] else None
        if best:
            block, score, triplets, answer = best
            save_search(
                filename=filename, question=question, answer=answer, confidence=score
            )

    return all_results, resolved_text, coref_map
