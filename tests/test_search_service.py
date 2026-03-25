from app.services.search_service import search
from app.nlp.answer_extraction import format_triplets

text = """
The boy kicked the ball because he was playing football.
The girl ran home.
The dog barked loudly.
The sun was Shining and the boy saw the girl with his ball. 
She gave him the ball.
"""

results = search(
    questions=["Who kicked the ball?", "Who gave the ball?", "Why did boy kicked the ball?"],
    text=text,
    top_k=1
)

for question, hits in results.items():
    print(f"\nQ: {question}")
    if not hits:
        print("  A: No answer found.")
        continue
    block, score, triplets, answer = hits[0]
    print(f"  A: {answer or '—'} ({score:.0%})")