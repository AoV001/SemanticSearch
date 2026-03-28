

from app.services.search_service import search
from app.db.database import init_db
init_db()

text = """
Last summer, Emma decided to try something new. Instead of spending her vacation at home, she joined a volunteer program in a small village near the mountains. The village was beautiful but very quiet, and many young people had moved away to bigger cities.
Emma and other volunteers worked together to repair an old community center. Every morning they painted walls, fixed broken windows, and cleaned the yard around the building. In the afternoons, they organized activities for local children, such as drawing, playing games, and reading stories.

At first, Emma was worried because she didn’t know anyone there. However, after a few days she began to feel comfortable. The volunteers became good friends, and the villagers were very kind and grateful for their help.

One evening, the village organized a small celebration to thank the volunteers. There was traditional food, music, and dancing. Emma realized that although the work was sometimes difficult, the experience was unforgettable.

When she returned home, Emma felt proud of what she had done. She also learned that helping others can be one of the most rewarding experiences in life.
"""


questions = [
    "When did Emma join the volunteer program?",
    "Where was the village located?",
    "What building did the volunteers repair?",
    "What did they do every morning?",
    "What activities did they organize for the children?",
    "Why was Emma worried at the beginning?",
    "How did the villagers feel about the volunteers?",
    "What happened one evening in the village?",
]


results, resolved_text, coref_map = search(questions=questions, text=text, top_k=1, threshold=0.3)

print("\n" + "="*60)
print("SEARCH LOGIC TEST")
print("="*60)

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