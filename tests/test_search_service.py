from app.services.search_service import search

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
    print(f"\n{score:.2f} - {block}")
    if answer:
        print(f"  Answer: {answer}")
    print("  Relevant connections:")
    for u, rel, v in triplets:
        print(f"    {u} --[{rel}]--> {v}")
