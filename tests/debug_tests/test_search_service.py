from app.services.search_service import search

text = """
The boy kicked the ball because he was playing football for 2 hours.
The girl ran home after she saw him.
The dog barked loudly before it got to sleep.
The sun was Shining and the boy saw the girl with his ball. 
She gave him the ball.
"""

results = search(
    questions=[
        "Who kicked the ball?",
        "Who gave the ball?",
        "Why did boy kicked the ball?",
        "What happened before the girl ran home? ",
        "What happened after the girl saw the boy? ",
        "What happened before the dog got to sleep?",
        "What happened after the dog barked loudly? ",
        "How long did the boy play football?",
    ],
    text=text,
    top_k=1,
)

for question, hits in results.items():
    print(f"\nQ: {question}")
    if not hits:
        print("  A: No answer found.")
        continue
    block, score, triplets, answer = hits[0]
    print(f"  A: {answer or '—'} ({score:.0%})")
