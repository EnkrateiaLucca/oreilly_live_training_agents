"""Simplified research-report agent — runnable demo.

This is the realistic-shape sibling of the
`3.0-local-research-agent-langgraph.ipynb` notebook. The notebook
prioritizes pedagogy (Ollama, inline cells, JSON parsing); this module
prioritizes the layout you would actually ship:

    generate_query  →  web_research  →  reflect  ──┐
                          ▲                        │ is_sufficient?
                          └──── loop ──────────────┤
                                                   ▼
                                       compress_notes  →  write_report  →  END

Run from the repo root with the LangGraph CLI:

    langgraph dev

Then open LangGraph Studio and invoke with:

    {"research_topic": "Recent advances in retrieval-augmented generation"}

Required environment variables:
    OPENAI_API_KEY   — chat model + structured outputs
    TAVILY_API_KEY   — web search

Optional:
    LANGSMITH_API_KEY, LANGSMITH_TRACING=true — traces in LangSmith
"""

from datetime import datetime
from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from tavily import TavilyClient

from demos.research_agent.models import (
    Reflection,
    ResearchInput,
    ResearchOutput,
    ResearchState,
    SearchQuery,
)
from demos.research_agent.prompts import (
    COMPRESS_NOTES_PROMPT,
    QUERY_WRITER_PROMPT,
    REFLECTION_PROMPT,
    WRITE_REPORT_PROMPT,
)


# =====================================================================
# Configuration
# =====================================================================
# Hardcoded for clarity — in production you would pass these through
# `RunnableConfig.configurable`. Mirrors the educational style of
# langchain-ai/langgraph-101's `researcher/graph.py`.

RESEARCH_MODEL = "openai:gpt-4.1-mini"
MAX_RESEARCH_LOOPS = 3              # Cap iterations so demos stay cheap.
MAX_RESULTS_PER_SEARCH = 3          # Tavily results per query.
MAX_TOKENS_PER_SOURCE = 1000        # Rough budget per source in chars/4.


# =====================================================================
# Helpers
# =====================================================================


def get_today_str() -> str:
    """Today's date as a short human-readable string.

    Injected into every prompt so the model knows what "recent" means
    and does not confuse last year's data for current.
    """
    now = datetime.now()
    return f"{now:%a} {now:%b} {now.day}, {now:%Y}"


def _format_search_results(results: dict) -> tuple[str, list[str]]:
    """Format Tavily results into (note_text, source_urls).

    Note text is truncated per source so a single long page cannot blow
    out the context window. Returning sources separately makes citation
    in the final report trivial.
    """
    notes_parts = []
    urls = []
    seen = set()

    for item in results.get("results", []):
        url = item.get("url", "")
        if url in seen:
            continue
        seen.add(url)
        urls.append(f"{item.get('title', 'Untitled')} — {url}")

        raw = item.get("raw_content") or item.get("content") or ""
        char_limit = MAX_TOKENS_PER_SOURCE * 4
        if len(raw) > char_limit:
            raw = raw[:char_limit] + "... [truncated]"

        notes_parts.append(
            f"### {item.get('title', 'Untitled')}\n"
            f"URL: {url}\n\n"
            f"{raw}\n"
        )

    return "\n---\n".join(notes_parts), urls


def _get_model():
    """Build the chat model. Centralized so the model swap is a one-liner."""
    return init_chat_model(model=RESEARCH_MODEL, temperature=0)


# =====================================================================
# Nodes
# =====================================================================


def generate_query(state: ResearchState, config: RunnableConfig) -> dict:
    """Turn the research topic (or the latest reflection) into a search query.

    Uses `.with_structured_output(SearchQuery)` so we get a typed
    `SearchQuery` object back — no JSON parsing, no defensive code.
    """
    model = _get_model().with_structured_output(SearchQuery)
    prompt = QUERY_WRITER_PROMPT.format(
        today=get_today_str(),
        research_topic=state.research_topic,
    )
    result: SearchQuery = model.invoke(prompt)
    return {"search_query": result.query}


def web_research(state: ResearchState) -> dict:
    """Execute the current search query and append the results to state."""
    client = TavilyClient()
    raw = client.search(
        state.search_query,
        max_results=MAX_RESULTS_PER_SEARCH,
        include_raw_content=True,
    )
    note_text, source_urls = _format_search_results(raw)
    return {
        "raw_notes": state.raw_notes + [note_text],
        "sources": state.sources + source_urls,
        "loop_count": state.loop_count + 1,
    }


def reflect(state: ResearchState) -> dict:
    """Decide whether we have enough information or need to loop.

    The `Reflection` schema forces the model to commit to a boolean
    `is_sufficient` — this is the routing signal `should_continue`
    reads. Without the structured output the model tends to hedge,
    which makes routing decisions noisy.
    """
    model = _get_model().with_structured_output(Reflection)
    prompt = REFLECTION_PROMPT.format(
        today=get_today_str(),
        research_topic=state.research_topic,
        notes="\n\n".join(state.raw_notes),
    )
    result: Reflection = model.invoke(prompt)
    return {"search_query": result.follow_up_query}


def should_continue(state: ResearchState) -> Literal["web_research", "compress_notes"]:
    """Stop on loop budget; otherwise keep researching.

    Note: we intentionally do NOT also re-read `Reflection.is_sufficient`
    here — that would require re-running the model. Instead `reflect`
    could be extended later to set a state flag. For an intro demo, the
    hard loop cap is the right teaching shape: clear, deterministic, and
    easy to reason about.
    """
    if state.loop_count >= MAX_RESEARCH_LOOPS:
        return "compress_notes"
    return "web_research"


def compress_notes(state: ResearchState) -> dict:
    """Dedupe and dense-pack raw notes before the writer sees them.

    Two-stage compress→write is from langchain-ai/langgraph-101. The
    writer prompt is far shorter and produces a cleaner report when its
    input is already organized.
    """
    model = _get_model()
    prompt = COMPRESS_NOTES_PROMPT.format(
        today=get_today_str(),
        research_topic=state.research_topic,
        raw_notes="\n\n".join(state.raw_notes),
    )
    result = model.invoke(prompt)
    return {"compressed_notes": result.content}


def write_report(state: ResearchState) -> dict:
    """Produce the final markdown report."""
    model = _get_model()
    prompt = WRITE_REPORT_PROMPT.format(
        today=get_today_str(),
        research_topic=state.research_topic,
        compressed_notes=state.compressed_notes or "",
    )
    result = model.invoke(prompt)

    sources_block = "\n".join(f"- {s}" for s in state.sources)
    final = f"{result.content}\n\n## Sources\n{sources_block}"
    return {"final_report": final}


# =====================================================================
# Graph
# =====================================================================

_builder = StateGraph(ResearchState, input=ResearchInput, output=ResearchOutput)

_builder.add_node("generate_query", generate_query)
_builder.add_node("web_research", web_research)
_builder.add_node("reflect", reflect)
_builder.add_node("compress_notes", compress_notes)
_builder.add_node("write_report", write_report)

_builder.add_edge(START, "generate_query")
_builder.add_edge("generate_query", "web_research")
_builder.add_edge("web_research", "reflect")
_builder.add_conditional_edges("reflect", should_continue)
_builder.add_edge("compress_notes", "write_report")
_builder.add_edge("write_report", END)

graph = _builder.compile()
