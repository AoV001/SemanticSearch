from spacy.lang.en import English
from app.graph.graph_similarity import graph_similarity, extract_relevant_subgraph
from app.nlp.answer_extraction import (
    extract_answer,
    extract_temporal_answer,
    TEMPORAL_MARKERS,
)
from app.cache.graph_cache import get_graph
from app.nlp.coreference import get_coreference_map
from typing import List
from app.db.history import save_search
from app.cache.graph_cache import get_resolved
from app.rag.retriever import retrieve
from app.rag.generator import generate_answer

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
GRAPH_RAG_CONTEXT_LIMIT = 2
GRAPH_RAG_CONFIDENCE_THRESHOLD = 0.9


def split_blocks(sentences, window_size=WINDOW_SIZE):
    if not sentences:
        return []
    if len(sentences) <= window_size:
        return [" ".join(sentences)]

    blocks = []
    for i in range(len(sentences) - window_size + 1):
        block = " ".join(sentences[i : i + window_size])
        blocks.append(block)
    return blocks


def search(
    questions: List[str],
    text: str,
    top_k: int = 3,
    threshold=0.3,
    filename: str = "",
    mode: str = "graph",
    include_metadata: bool = False,
):
    mode = getattr(mode, "value", mode)
    if mode not in {"graph", "rag", "graph_rag"}:
        raise ValueError(f"Unsupported search mode: {mode}")

    nlp_sent = English()
    nlp_sent.add_pipe("sentencizer")
    cleaned_text = text.replace("\n", " ")
    doc = nlp_sent(cleaned_text)

    sentences = [sent.text.strip() for sent in doc.sents]
    blocks = split_blocks(sentences, window_size=WINDOW_SIZE)
    resolved_text = get_resolved(cleaned_text)
    coref_map = get_coreference_map(cleaned_text)
    all_results = {}

    resolved_blocks = [get_resolved(block) for block in blocks] if mode != "rag" else []

    for question in questions:
        question_graph = get_graph(question)
        results = []

        if mode in {"graph", "graph_rag"}:
            ranked_blocks = []
            for original_block, resolved_block in zip(blocks, resolved_blocks):
                block_graph = get_graph(resolved_block)
                score = graph_similarity(question_graph, block_graph)
                if score >= threshold:
                    ranked_blocks.append((original_block, resolved_block, score))
        else:
            ranked_blocks = [
                (chunk.text, get_resolved(chunk.text), chunk.score)
                for chunk in retrieve(filename, text, question, top_k)
            ]

        ranked_blocks.sort(key=lambda item: item[2], reverse=True)
        generated_answer = None
        if mode == "rag":
            generated_answer = generate_answer(
                question, [resolved_block for _, resolved_block, _ in ranked_blocks]
            )

        for result_number, (original_block, resolved_block, score) in enumerate(
            ranked_blocks
        ):
            block_graph = get_graph(resolved_block)
            triplets = extract_relevant_subgraph(question_graph, block_graph, hop=1)
            extracted_answer = extract_answer(
                triplets, question_graph, resolved_block, original_question=question
            )
            is_temporal = any(m in question.lower() for m in ALL_TEMPORAL)
            if is_temporal:
                temporal = extract_temporal_answer(resolved_block, question)
                if temporal:
                    extracted_answer = temporal
            answer = (
                generated_answer
                if mode == "rag" and generated_answer and result_number == 0
                else extracted_answer
            )
            # Return source text so the UI can always highlight it exactly.
            llm_used = mode == "rag" and result_number == 0 and bool(generated_answer)
            source = "RAG LLM" if llm_used else "Graph extraction"
            results.append((original_block, score, triplets, answer, source, llm_used))

        if mode == "graph_rag" and results:
            best_block, best_score, best_triplets, best_answer, _, _ = results[0]
            if best_score < GRAPH_RAG_CONFIDENCE_THRESHOLD or not best_answer:
                generated_answer = generate_answer(
                    question,
                    [
                        original_block
                        for original_block, _, _ in ranked_blocks[
                            :GRAPH_RAG_CONTEXT_LIMIT
                        ]
                    ],
                )
                if generated_answer:
                    results[0] = (
                        best_block,
                        best_score,
                        best_triplets,
                        generated_answer,
                        "GraphRAG LLM",
                        True,
                    )

        results.sort(key=lambda x: x[1], reverse=True)
        all_results[question] = results[:top_k]

        best = all_results[question][0] if all_results[question] else None
        if best:
            block, score, triplets, answer, _, _ = best
            save_search(
                filename=filename, question=question, answer=answer, confidence=score
            )

    if not include_metadata:
        all_results = {
            question: [result[:4] for result in hits]
            for question, hits in all_results.items()
        }
    return all_results, resolved_text, coref_map
