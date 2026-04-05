from app.graph.graph_builder import build_dependency_graph

question = "What major change in the workplace is described in the text?"
block = "In recent years, the way people work has changed dramatically. One of the biggest changes has been the rise of remote work."

qg = build_dependency_graph(question)
bg = build_dependency_graph(block)

print("Question nodes:", {d["lemma"] for _, d in qg.nodes(data=True)})
print("Block nodes:", {d["lemma"] for _, d in bg.nodes(data=True)})
print(
    "Question edges:",
    {(qg.nodes[u].get("lemma"), qg.nodes[v].get("lemma")) for u, v in qg.edges()},
)
print(
    "Block edges:",
    {(bg.nodes[u].get("lemma"), bg.nodes[v].get("lemma")) for u, v in bg.edges()},
)
