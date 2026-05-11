# Testing Guide — O'Reilly LangGraph Course

This guide lets you quickly set up the environment and run every notebook to verify it executes without errors.

---

## 1. Environment Setup

### Option A: uv (recommended)

```bash
uv venv .venv
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate           # Windows

uv pip install -r requirements/requirements.txt
python -m ipykernel install --user --name=oreilly-agents --display-name "Python (oreilly-agents)"
```

### Option B: venv

```bash
python3 -m venv oreilly-agents
source oreilly-agents/bin/activate          # Linux/Mac
# .\oreilly-agents\Scripts\activate         # Windows

pip install -r requirements/requirements.txt
python -m ipykernel install --user --name=oreilly-agents --display-name "Python (oreilly-agents)"
```

### Option C: Conda

```bash
conda create -n oreilly-agents python=3.11 -y
conda activate oreilly-agents
pip install -r requirements/requirements.txt
python -m ipykernel install --user --name=oreilly-agents --display-name "Python (oreilly-agents)"
```

### Additional packages for new notebooks

```bash
# For SqliteSaver (notebook 5.0)
uv pip install langgraph-checkpoint-sqlite

# For MCP integration (notebook 4.0)
uv pip install langchain-mcp-adapters
```

---

## 2. API Keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

Required keys:

| Variable | Required by | Where to get it |
|----------|-------------|-----------------|
| `OPENAI_API_KEY` | All notebooks (0.0–4.0) | https://platform.openai.com/ |
| `LANGCHAIN_API_KEY` | Notebook 3.0 (tracing, optional) | https://smith.langchain.com/ |

Notebooks that use local Ollama models (3.0) also require Ollama installed and the model pulled — see section 4 below.

---

## 3. Running Every Notebook with nbconvert

Use `nbconvert` to execute each notebook non-interactively. This is the canonical way to verify a notebook runs end-to-end.

**Single notebook:**
```bash
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=120 \
  notebooks/1.0-intro-langgraph.ipynb \
  --output /tmp/1.0-executed.ipynb
```

**All notebooks at once (bash loop):**
```bash
for nb in notebooks/0.0-intro-llm-agents-from-scratch.ipynb \
           notebooks/1.0-intro-langgraph.ipynb \
           notebooks/1.1-simple-react-agent-langgraph.ipynb \
           notebooks/2.0-langgraph-core-concepts.ipynb \
           notebooks/3.0-local-research-agent-langgraph.ipynb \
           notebooks/4.0-langgraph-latest.ipynb \
           notebooks/5.0-persistence-and-checkpointers.ipynb \
           notebooks/6.0-subgraphs.ipynb \
           notebooks/7.0-deployment-langgraph-platform.ipynb; do
  name=$(basename "$nb" .ipynb)
  echo "Running $name..."
  jupyter nbconvert --to notebook --execute \
    --ExecutePreprocessor.timeout=120 \
    "$nb" \
    --output "/tmp/${name}-executed.ipynb" 2>&1 | tail -3
  echo "---"
done
```

Inspect results:
```bash
# Check for errors in a specific executed notebook
python3 -c "
import json, sys
nb = json.load(open('/tmp/1.0-executed.ipynb'))
errors = [
    (i, o['evalue'])
    for i, cell in enumerate(nb['cells'])
    for o in cell.get('outputs', [])
    if o.get('output_type') == 'error'
]
if errors:
    for i, e in errors: print(f'Cell {i}: {e}')
else:
    print('No errors')
"
```

---

## 4. Expected Failures & How to Handle Them

| Notebook | Cell | Expected failure | Fix |
|----------|------|-----------------|-----|
| 0.0–4.0 | Any OpenAI call | `AuthenticationError` or `openai.APIError` | Set `OPENAI_API_KEY` in `.env` |
| 3.0 | Research agent cells | `ResponseError: model 'llama3' not found` | Run `ollama pull llama3` (or whichever model is configured) |
| 3.0 | `os.environ["LANGCHAIN_API_KEY"]` | Warning if key missing | Optional — only needed for LangSmith tracing |
| 5.0 | SqliteSaver import | `ModuleNotFoundError` | `pip install langgraph-checkpoint-sqlite` |
| 4.0 | MCP section | Print message (cell is commented out) | Expected — requires a running MCP server |
| 7.0 | All cells | Markdown-only, no execution | Expected — deployment steps are documentation |

### Ollama setup (for notebook 3.0)

```bash
# Install Ollama: https://ollama.com
# Then pull the required model:
ollama pull llama3

# Verify it's available:
ollama list
```

---

## 5. Quick Smoke Test (no API key needed)

These notebooks have cells that run without any API key:

```bash
# 5.0 — persistence with InMemorySaver (no API key needed)
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=60 \
  notebooks/5.0-persistence-and-checkpointers.ipynb \
  --output /tmp/5.0-executed.ipynb

# 6.0 — subgraphs (no API key needed)
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=60 \
  notebooks/6.0-subgraphs.ipynb \
  --output /tmp/6.0-executed.ipynb
```

These two are good first checks that the environment and langgraph install are working.

---

## 6. Verifying notebook JSON integrity

Before opening in Jupyter, confirm files are valid JSON:

```bash
python3 -c "
import json, glob, sys
for path in sorted(glob.glob('notebooks/*.ipynb')):
    try:
        json.load(open(path))
        print(f'OK  {path}')
    except Exception as e:
        print(f'ERR {path}: {e}')
        sys.exit(1)
"
```
