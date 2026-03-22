from app.services.search_service import search


text = """
The Boy kicked the ball. He ran after it.
The girl ran home.
The dog barked loudly.
The sun was Shining and the Boy saw the Girl with his ball. 
She gave him the ball.
"""

question = "Who kicked the ball?"

results = search(question, text)

for sentence, score in results:
    print(score, sentence)