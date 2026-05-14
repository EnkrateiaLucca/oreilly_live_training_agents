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

| File | Responsibility |
|------|----------------|
| `models.py`  | Pydantic state + structured-output schemas (`SearchQuery`, `Reflection`) |
| `prompts.py` | Named prompt constants, one per node |
| `graph.py`   | Nodes, edges, compiled `graph` object |
| `langgraph.json` | LangGraph CLI config for `langgraph dev` / Studio |

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

## Running

From the project root (`oreilly_live_training_agents/`):

```bash
# 1. Install the LangGraph CLI if you haven't already
pip install -U "langgraph-cli[inmem]"

# 2. Set environment variables
export OPENAI_API_KEY=sk-...
export TAVILY_API_KEY=tvly-...

# 3. Launch Studio
cd demos/research_agent
langgraph dev
```

Then invoke from the Studio UI with:

```json
{ "research_topic": "Recent advances in retrieval-augmented generation" }
```

Or call it directly from Python:

```python
from demos.research_agent import graph

result = graph.invoke({
    "research_topic": "Recent advances in retrieval-augmented generation",
})
print(result["final_report"])
```
