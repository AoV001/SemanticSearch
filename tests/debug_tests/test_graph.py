from app.graph.graph_builder import build_dependency_graph

sentence = "The boy kicked the ball"

graph = build_dependency_graph(sentence)

print("Nodes:")
print(graph.nodes(data=True))

print("\nEdges:")
print(graph.edges(data=True))
