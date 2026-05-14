# O'Reilly Live Training - Getting Started with LLM Agents using LangChain & LangGraph

## Quick Setup (Recommended: uv)

The fastest way to get started is using [uv](https://github.com/astral-sh/uv), a modern Python package manager:

1. **Install uv:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create and activate virtual environment:**
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -r requirements/requirements.txt
   ```

4. **Set up your environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Install Jupyter kernel for this project:**
   ```bash
   python -m ipykernel install --user --name=oreilly-agents --display-name "O'Reilly Agents (oreilly-agents)"
   ```

## Alternative Setup Methods

### Using Conda

- Install [anaconda](https://www.anaconda.com/download)
- Create an environment: `conda create -n oreilly-agents python=3.11`
- Activate your environment with: `conda activate oreilly-agents`
- Install requirements with: `pip install -r requirements/requirements.txt`
- Setup your openai [API key](https://platform.openai.com/)

### Using Pip

1. **Create a Virtual Environment:**
    Navigate to your project directory.
    If using Python 3's built-in `venv`: `python -m venv oreilly-agents`
    If you're using `virtualenv`: `virtualenv oreilly-agents`

2. **Activate the Virtual Environment:**
    - **On Windows:** `.\oreilly-agents\Scripts\activate`
    - **On macOS and Linux:** `source oreilly-agents/bin/activate`

3. **Install Dependencies from `requirements.txt`:**
    ```bash
    pip install -r ./requirements/requirements.txt
    ```

Remember to deactivate the virtual environment afterwards: `deactivate`

## Setup your .env file

Copy the `.env.example` file to `.env` and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env` and add your keys:
- **OPENAI_API_KEY** (required): Get it at https://platform.openai.com/api-keys
- **TAVILY_API_KEY** (required for web search): Get it at https://tavily.com/
- **ANTHROPIC_API_KEY** (optional): Get it at https://platform.claude.com/settings/keys
- **LANGSMITH_API_KEY** (optional): Get it at https://smith.langchain.com/settings
- **SERPAPI_KEY** (optional): Get it at https://serpapi.com/ (for Google search)

## Using Jupyter Notebooks

### Selecting the Correct Kernel

**Important:** When opening notebooks in VS Code or Jupyter, you must select the correct kernel:

1. Open any `.ipynb` notebook file
2. Click on the kernel selector (top-right in VS Code, or top menu in Jupyter)
3. Select **"O'Reilly Agents (oreilly-agents)"** from the list
4. If you don't see it, make sure you installed the kernel (see setup step 5)

## Notebooks

### Core Learning Path

The main notebooks are organized in a progressive learning path:

0. [Intro to LLM Agents from Scratch](notebooks/0.0-intro-llm-agents-from-scratch.ipynb) - Building agents without frameworks
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/0.0-intro-llm-agents-from-scratch.ipynb)

1. [Intro to LangGraph](notebooks/1.0-intro-langgraph.ipynb) - Fundamentals of LangGraph
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.0-intro-langgraph.ipynb)

   - [1.1 Simple ReAct Agent with LangGraph](notebooks/1.1-simple-react-agent-langgraph.ipynb) - Quick start with a basic ReAct agent
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.1-simple-react-agent-langgraph.ipynb)

   - [1.2 LangGraph with ChatGPT Search](notebooks/1.2-intro-langgraph-chatgpt-search.ipynb) - Using search capabilities
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.2-intro-langgraph-chatgpt-search.ipynb)

2. [LangGraph Core Concepts](notebooks/2.0-langgraph-core-concepts.ipynb) - Deep dive into LangGraph concepts
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/2.0-langgraph-core-concepts.ipynb)

   - [2.1 LangGraph Basics](notebooks/2.1-langgraph-basics.ipynb) - Core LangGraph components and patterns
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/2.1-langgraph-basics.ipynb)

3. [Local Research Agent with LangGraph](notebooks/3.0-local-research-agent-langgraph.ipynb) - Building a research agent
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/3.0-local-research-agent-langgraph.ipynb)

4. [LangGraph Latest Features](notebooks/4.0-langgraph-latest.ipynb) - Command, subgraphs, Functional API, MCP, durable execution
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/4.0-langgraph-latest.ipynb)

5. [Persistence and Checkpointers](notebooks/5.0-persistence-and-checkpointers.ipynb) - InMemorySaver, SqliteSaver, thread management, state inspection
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/5.0-persistence-and-checkpointers.ipynb)

6. [Subgraphs](notebooks/6.0-subgraphs.ipynb) - Composing graphs, shared-state and different-schema patterns, multi-agent building blocks
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/6.0-subgraphs.ipynb)

7. [Deployment with LangGraph Platform](notebooks/7.0-deployment-langgraph-platform.ipynb) - Project structure, `langgraph dev`, deploying to LangSmith
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/7.0-deployment-langgraph-platform.ipynb)

## Repository Structure

```
├── notebooks/                      # Main learning notebooks
│   ├── assets-resources/          # Images, diagrams, and research papers
│   ├── langgraph-app/            # LangGraph deployment example
│   ├── langgraph-mcp-quick-demo/ # Model Context Protocol demo
│   ├── legacy-notebooks/         # Previous course materials
│   └── legacy-scripts/           # Utility scripts and examples
├── presentation-slides/           # Course presentation materials (PDFs)
├── requirements/                  # Python dependencies
└── docs/                         # Additional documentation
```

## Additional Resources

- **Presentation Slides**: Course slides available in `presentation-slides/` folder
  - Getting Started with LangGraph
  - Getting Started with Agents Using LangChain
  - Intro LLM Agents

- **Deployment Example**: Check `notebooks/langgraph-app/` for a complete LangGraph deployment setup

- **MCP Demo**: See `notebooks/langgraph-mcp-quick-demo/` for Model Context Protocol integration examples

- **Legacy Materials**: Previous course content available in `notebooks/legacy-notebooks/` and `notebooks/legacy-scripts/`
