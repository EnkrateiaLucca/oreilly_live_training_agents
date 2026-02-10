# O'Reilly Live Training - Getting Started with LLM Agents using LangChain & LangGraph

## Setup

**Conda**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.11.
- Create an environment: `conda create -n oreilly-agents python=3.11`
- Activate your environment with: `conda activate oreilly-agents`
- Install requirements with: `pip install -r requirements/requirements.txt`
- Setup your openai [API key](https://platform.openai.com/)

**Pip**

1. **Create a Virtual Environment:**
    Navigate to your project directory. Make sure you have python3.10 installed!
    If using Python 3's built-in `venv`: `python -m venv oreilly-agents`
    If you're using `virtualenv`: `virtualenv oreilly-agents`

2. **Activate the Virtual Environment:**
    - **On Windows:** `.\\oreilly-agents\\Scripts\\activate`
    - **On macOS and Linux:** `source oreilly-agents/bin/activate`

3. **Install Dependencies from `requirements.txt`:**
    ```bash
    pip install python-dotenv
    pip install -r ./requirements/requirements.txt
    ```

4. Setup your openai [API key](https://platform.openai.com/)

Remember to deactivate the virtual environment afterwards: `deactivate`

## Setup your .env file

- Change the `.env.example` file to `.env` and add your OpenAI API key.

```bash
OPENAI_API_KEY=<your openai api key>
```

## To use this Environment with Jupyter Notebooks:

```bash
conda install jupyter -y
python -m ipykernel install --user --name=oreilly-agents
```

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

4. [LangGraph Latest Features](notebooks/4.0-langgraph-latest.ipynb) - Latest LangGraph features and patterns
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/4.0-langgraph-latest.ipynb)

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
