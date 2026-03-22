from app.services.search_service import search
from app.nlp.coreference import simple_coreference


text = """
The Boy kicked the ball. He ran after it.
The girl ran home.
The dog barked loudly.
The sun was Shining and the Boy saw the Girl with his ball. 
She gave him the ball.
"""

question = "Who kicked the ball?"

results = search(question, text, top_k=5)

for score, (sentence, sim) in enumerate(results):
    print(f"{sim:.2f} - {sentence}")

resolved = simple_coreference(text)
print(resolved)