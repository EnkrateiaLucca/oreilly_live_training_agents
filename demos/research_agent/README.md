# Research Agent — Runnable Demo

The realistic-shape sibling of `notebooks/3.0-local-research-agent-langgraph.ipynb`.

The notebook walks you through the agent cell-by-cell with Ollama. This
package is what the same agent looks like once you split it into the
files you would actually ship: one for state, one for prompts, one for
graph wiring.

## Architecture

```
generate_query  →  web_research  →  reflect  ──┐
                       ▲                        │ loop_count < MAX?
                       └──── loop ──────────────┤
                                                ▼
                                    compress_notes  →  write_report  →  END
```

## Project layout

This is the standard LangGraph Platform layout (see
`notebooks/4.0-deployment-langgraph-platform.ipynb`):

```
research_agent/
├── langgraph.json            # Deployment manifest: graphs, deps, env
├── pyproject.toml            # Makes src/research_agent an installable package
├── .env                      # API keys (gitignored; see .env.example)
└── src/research_agent/
    ├── graph.py              # Nodes, edges, compiled `graph` object
    ├── models.py             # Pydantic state + structured-output schemas
    └── prompts.py            # Named prompt constants, one per node
```

## Architectural choices worth noticing

1. **Structured outputs everywhere.** Every LLM-as-decision-maker call uses
   `.with_structured_output(PydanticModel)`. No `json.loads()`, no parse
   failures.
2. **Two-stage write.** Raw notes → `compress_notes` → `write_report`.
   Compression strips boilerplate so the writer sees dense, organized
   input. Borrowed from `langchain-ai/langgraph-101`.
3. **Public input/output schemas.** `ResearchState` is private working
   memory; `ResearchInput` / `ResearchOutput` define the public contract.
4. **Hardcoded configuration block.** Tunable knobs live at the top of
   `graph.py` instead of being threaded through `RunnableConfig`. In a
   teaching context, this is much easier to point at and explain.

## Running locally (LangGraph Studio)

```bash
# 1. Install the LangGraph CLI if you haven't already
pip install -U "langgraph-cli[inmem]"

# 2. Provide API keys (copy .env.example → .env, or symlink the repo root .env)
cp .env.example .env   # then fill in OPENAI_API_KEY and TAVILY_API_KEY

# 3. Launch the dev server (from this directory)
langgraph dev --no-reload
```

> `--no-reload`: the in-memory runtime persists its store to
> `.langgraph_api/*.pckl` inside this directory, which retriggers the
> file-watcher and hot-reloads the server mid-run (killing active
> streams). Disable reloading for demos; restart manually after code
> changes.

`langgraph dev` reads `langgraph.json`, serves the graph on
`http://127.0.0.1:2024`, and opens LangGraph Studio in your browser.
Invoke from the Studio UI with:

```json
{ "research_topic": "Recent advances in retrieval-augmented generation" }
```

Or call it directly from Python:

```python
from research_agent import graph   # pip install -e . first

result = graph.invoke({
    "research_topic": "Recent advances in retrieval-augmented generation",
})
print(result["final_report"])
```

## Deploying

When you're ready to ship, the same `langgraph.json` drives the
production deployment (LangSmith Deployments / Cloud SaaS):

```bash
langgraph deploy
```
