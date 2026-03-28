

from app.services.search_service import search
from app.db.database import init_db
from app.services.search_service import split_blocks
from app.nlp.coreference import simple_coreference
from app.graph.graph_builder import build_dependency_graph
from app.graph.graph_similarity import graph_similarity
from spacy.lang.en import English

init_db()

text = """
Last summer, Emma decided to try something new. Instead of spending her vacation at home, she joined a volunteer program in a small village near the mountains. The village was beautiful but very quiet, and many young people had moved away to bigger cities.
Emma and other volunteers worked together to repair an old community center. Every morning they painted walls, fixed broken windows, and cleaned the yard around the building. In the afternoons, they organized activities for local children, such as drawing, playing games, and reading stories.

At first, Emma was worried because she didn’t know anyone there. However, after a few days she began to feel comfortable. The volunteers became good friends, and the villagers were very kind and grateful for their help.

One evening, the village organized a small celebration to thank the volunteers. There was traditional food, music, and dancing. Emma realized that although the work was sometimes difficult, the experience was unforgettable.

When she returned home, Emma felt proud of what she had done. She also learned that helping others can be one of the most rewarding experiences in life.
"""


questions = [
    "What activities did they organize for the children?",
]
results, resolved_text, coref_map = search(questions=questions, text=text, top_k=3, threshold=0.1)

print("\n" + "="*60)
print("SEARCH LOGIC TEST")
print("="*60)

nlp_sent = English()
nlp_sent.add_pipe("sentencizer")
doc = nlp_sent(text.replace("\n", " "))
sentences = [sent.text.strip() for sent in doc.sents]
blocks = split_blocks(sentences)
resolved_blocks = [simple_coreference(block) for block in blocks]

question = "What activities did they organize for the children?"
qg = build_dependency_graph(question)

for i, block in enumerate(resolved_blocks):
    bg = build_dependency_graph(block)
    score = graph_similarity(qg, bg)
    print(f"\nBlock {i} (score={score:.2f}):")
    print(f"  {block[:100]}")

for question, hits in results.items():
    print(f"\nQ: {question}")
    if not hits:
        print("  ❌ No answer found (threshold not met)")
        continue
    block, score, triplets, answer = hits[0]
    status = "✅" if answer and answer != "—" else "⚠️"
    print(f"  {status} A: {answer or '—'}")
    print(f"     Score: {score:.2f}")
    print(f"     Block: {block[:80]}...")
    if triplets:
        print(f"     Triplets: {[(u, r, v) for u, r, v in triplets[:3]]}")