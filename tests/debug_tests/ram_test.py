import time
import tracemalloc
from app.services.search_service import search
from app.db.database import init_db

init_db()

text = """In recent years, the way people work has changed dramatically. One of the biggest changes has been the rise of remote work. Thanks to modern technology, many employees no longer need to travel to an office every day. Instead, they can work from home, from a café, or even from another country.

For many workers, remote work offers significant advantages. It allows people to save time because they do not need to commute. In large cities, commuting can take several hours a day, so working remotely can greatly improve a person’s quality of life. In addition, employees often have more flexibility in organizing their schedules.

However, remote work also has its challenges. Some people find it difficult to separate their professional and personal lives when both take place in the same space. Others may feel isolated because they have fewer face-to-face interactions with colleagues.

Companies are still trying to find the best balance between remote and office work. Some organizations prefer a hybrid model, where employees work from home a few days a week and come to the office on other days. This approach allows workers to enjoy flexibility while still maintaining personal contact with their teams.

As technology continues to develop, experts believe that remote work will remain an important part of the modern workplace. The challenge for both employers and employees will be learning how to use this system in a healthy and productive way."""

questions = [
    "What major change in the workplace is described in the text?",
    "What technology has made remote work possible?",
    "Why can remote work improve people’s quality of life?",
    "What is one benefit related to employees’ schedules?",
    "What problem can occur when people work and live in the same place?",
    "Why might remote workers feel isolated?",
    "What solution are some companies using to solve the problems of remote work?",
    "What is a hybrid work model?",
    "According to experts, what will happen to remote work in the future?",
    "What challenge will employers and employees face?",
]

# RAM
tracemalloc.start()

# Время
start = time.perf_counter()
results, resolved_text, coref_map = search(questions=questions, text=text, top_k=3)
elapsed = time.perf_counter() - start

# RAM
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"\nTime:     {elapsed:.3f}s")
print(f"RAM now:  {current / 1024:.1f} KB")
print(f"RAM peak: {peak / 1024:.1f} KB")
print(f"Questions: {len(questions)}")
print(f"Text length: {len(text)} chars")

# Второй запуск — кэш уже заполнен
start2 = time.perf_counter()
tracemalloc.start()

results2, _, _ = search(questions=questions, text=text, top_k=3)

elapsed2 = time.perf_counter() - start2
current2, peak2 = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("\n--- Second run (cached) ---")
print(f"Time:     {elapsed2:.3f}s")
print(f"RAM peak: {peak2 / 1024:.1f} KB")
