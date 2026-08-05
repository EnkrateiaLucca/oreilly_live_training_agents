"""Pydantic models for the research agent.

Two kinds of models live here:

1. Structured-output schemas — the shape we force the LLM to produce
   when we call `.with_structured_output(...)`. These replace ad-hoc
   `json.loads(response.content)` parsing with a typed contract.

2. The graph State — the dict that flows between nodes. We use a
   Pydantic `BaseModel` (instead of a `TypedDict`) so we can attach
   defaults and validation in one place.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# =====================================================================
# Structured-output schemas
# =====================================================================
# Each of these is passed to `llm.with_structured_output(Schema)` so the
# model is guaranteed to return parseable, validated data. No more
# defensive `try: json.loads(...) except ...` blocks scattered through
# the graph.


class SearchQuery(BaseModel):
    """A single web-search query the agent will execute."""

    query: str = Field(description="The query string to send to the search engine.")
    rationale: str = Field(
        description="Why this query was chosen — one sentence. Useful in logs/traces."
    )


class Reflection(BaseModel):
    """The agent's reflection after reading the latest research notes.

    Mirrors the `think_tool` pattern from langchain-ai/langgraph-101 —
    we force the model to write down what it learned and what is still
    missing before deciding to loop again.
    """

    knowledge_gap: str = Field(
        description="What is still unclear or missing from the current notes."
    )
    follow_up_query: str = Field(
        description="A self-contained next query that would close the gap."
    )
    is_sufficient: bool = Field(
        description="True if the notes already answer the research topic well "
        "enough that no further searches are needed.",
    )


# =====================================================================
# Graph state
# =====================================================================


class ResearchState(BaseModel):
    """The full state passed between nodes.

    Fields are append-only in spirit: each node returns a partial dict
    that LangGraph merges into the existing state. Lists use
    `default_factory=list` so the merge starts from an empty list, not
    from the (shared, mutable) class-level default.
    """

    # --- inputs ---
    research_topic: str = Field(description="The user's original research request.")

    # --- working memory ---
    search_query: Optional[str] = None
    raw_notes: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    loop_count: int = 0

    # --- outputs ---
    compressed_notes: Optional[str] = None
    final_report: Optional[str] = None


class ResearchInput(BaseModel):
    """Public input contract — only `research_topic` is required from callers."""

    research_topic: str


class ResearchOutput(BaseModel):
    """Public output contract — what callers receive."""

    final_report: str
