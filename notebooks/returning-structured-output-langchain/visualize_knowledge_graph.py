from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
import instructor
from graphviz import Digraph
import argparse

class Node(BaseModel):
    id: int
    label: str
    color: str

class Edge(BaseModel):
    source: int
    target: int
    label: str
    color: str = "black"

class KnowledgeGraph(BaseModel):
    nodes: List[Node] = Field(..., default_factory=list)
    edges: List[Edge] = Field(..., default_factory=list)

# Adds response_model to ChatCompletion
# Allows the return of Pydantic model rather than raw JSON
client = instructor.patch(OpenAI())

def generate_graph(input) -> KnowledgeGraph:
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "user",
                "content": f"Help me understand the following by describing it as a detailed knowledge graph: {input}",
            }
        ],
        response_model=KnowledgeGraph,
    )  # type: ignore

def visualize_knowledge_graph(kg: KnowledgeGraph):
    dot = Digraph(comment="Knowledge Graph")

    # Add nodes
    for node in kg.nodes:
        dot.node(str(node.id), node.label, color=node.color)

    # Add edges
    for edge in kg.edges:
        dot.edge(str(edge.source), str(edge.target), label=edge.label, color=edge.color)

    # Render the graph
    dot.render("knowledge_graph.gv", view=True)

def main():
    parser = argparse.ArgumentParser(description="Generate and visualize a knowledge graph based on a given prompt.")
    parser.add_argument("prompt", type=str, help="The prompt to generate the knowledge graph from.")
    args = parser.parse_args()

    graph: KnowledgeGraph = generate_graph(args.prompt)
    visualize_knowledge_graph(graph)
    print("Knowledge graph generated and visualized.")

if __name__ == "__main__":
    main()
