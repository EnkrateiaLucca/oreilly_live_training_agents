"""Prompts for the research agent.

Kept in their own file for three reasons:

1. **Readability** — `graph.py` becomes about control flow, not text.
2. **Versioning** — prompt diffs show up cleanly in git review.
3. **Reuse** — the same prompt can power a notebook cell, a CLI tool,
   or an eval run without copy-paste drift.

Every prompt expects to be formatted with named placeholders. Search
each docstring for `{placeholder}` to see what each one needs.
"""

# ---------------------------------------------------------------------
# Query generation
# ---------------------------------------------------------------------

QUERY_WRITER_PROMPT = """You are a research assistant generating a web-search query.

Today's date is {today}.

Research topic:
{research_topic}

Write ONE focused query that will surface the most useful sources on
this topic. Prefer specific, technical phrasing over broad keywords.
Include the year if the topic is time-sensitive."""


# ---------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------
# Mirrors the `think_tool` pattern from langchain-ai/langgraph-101 — the
# model has to explicitly name what is missing before we let it loop.

REFLECTION_PROMPT = """You are reviewing research notes about: {research_topic}

Today's date is {today}.

Current notes:
{notes}

Decide:
1. Is the information already sufficient to write a thorough report?
2. If not, what is the most important knowledge gap?
3. What single follow-up query would best close that gap?

Be honest about sufficiency — looping unnecessarily wastes tokens and
adds noise to the final report."""


# ---------------------------------------------------------------------
# Compression
# ---------------------------------------------------------------------
# Two-stage write pattern from langchain-ai/langgraph-101:
#   raw notes  →  compressed notes  →  final report
# Compression strips boilerplate and dedupes so the writer node sees a
# clean, dense input. This dramatically improves report quality.

COMPRESS_NOTES_PROMPT = """You are compressing research notes for a downstream report writer.

Today's date is {today}.

Research topic:
{research_topic}

Raw notes from web searches:
{raw_notes}

Your job:
- Keep every concrete fact, statistic, name, and date.
- Drop boilerplate ("according to the article…"), duplicates, and ads.
- Group related facts together.
- Preserve source URLs inline as `[source: <url>]` whenever a claim
  can be attributed.

Output a dense, well-organized brief — not prose, not a report yet."""


# ---------------------------------------------------------------------
# Final report
# ---------------------------------------------------------------------

WRITE_REPORT_PROMPT = """You are writing a research report.

Today's date is {today}.

Research topic:
{research_topic}

Compressed research brief:
{compressed_notes}

Produce a markdown report with:
- A short executive summary (3–5 sentences).
- 3–6 themed sections with `##` headers.
- A `## Sources` section at the end listing every URL referenced.

Cite sources inline using `[source: <url>]`. Do not invent facts; if
the brief does not support a claim, omit it."""
