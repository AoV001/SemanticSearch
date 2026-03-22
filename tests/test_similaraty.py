from app.graph.graph_builder import build_dependency_graph
from app.graph.graph_similarity import graph_similarity

s1 ="The boy kicked the ball."
s2 = "Who kicked the ball?"

g1 = build_dependency_graph(s1)
g2 = build_dependency_graph(s2)

score = graph_similarity(g1, g2)

print("Similarity:", score)

print("Graph 1 nodes:")
print(g1.nodes(data=True))

print("\nGraph 2 nodes:")
print(g2.nodes(data=True))