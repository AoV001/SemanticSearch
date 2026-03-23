from app.services.search_service import search
from app.nlp.answer_extraction import format_triplets

text = """
The boy kicked the ball because he was playing football.
The girl ran home.
The dog barked loudly.
The sun was Shining and the boy saw the girl with his ball. 
She gave him the ball.
"""

question = "Why did the boy kick the ball?"

results = search(question, text, top_k=5)

for i, (block, score, triplets, answer) in enumerate(results):
    print(f"\n{'='*50}")
    print(f"Relevance: {score:.0%}")
    print(f"Context:   {block}")
    if answer:
        print(f"Answer:    {answer}")
    readable = format_triplets(triplets)
    if readable:
        print(f"Key relationships:")
        for line in readable:
            print(f"  • {line}")
