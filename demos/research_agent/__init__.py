"""Simplified Research Agent demo for the LangGraph intro course.

This package is the runnable, closer-to-production counterpart to the
`3.0-local-research-agent-langgraph.ipynb` notebook. Where the notebook
prioritizes step-by-step learning, this package prioritizes the
file/folder layout you would actually use to ship a LangGraph agent.

Architecture:
    graph.py    — nodes, edges, and the compiled `graph` object
    models.py   — Pydantic state + structured-output schemas
    prompts.py  — named prompt constants, one per node
"""

from demos.research_agent.graph import graph

__all__ = ["graph"]
