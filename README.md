# O'Reilly Live Trainining - Getting Started with LLM Agents using LangChain

## Setup

**Conda**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.10.
- Create an environment: `conda create -n oreilly-agents python=3.10`
- Activate your environment with: `conda activate oreilly-agents`
- Install requirements with: `pip install -r requirements/requirements.txt`
- Setup your openai [API key](https://platform.openai.com/)

**Pip**


1. **Create a Virtual Environment:**
    Navigate to your project directory. Make sure you have python3.10 installed! 
    If using Python 3's built-in `venv`: `python -m venv oreilly-agents`
    If you're using `virtualenv`: `virtualenv oreilly-agents`

2. **Activate the Virtual Environment:**
    - **On Windows:**: `.\oreilly-agents\Scripts\activate`
    - **On macOS and Linux:**: `source oreilly-agents/bin/activate`

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

- ```conda install jupyter -y```
- ```python -m ipykernel install --user --name=oreilly-agents```

## Notebooks

Here are the notebooks available in the `notebooks/` folder:

1. [Intro LLM Agents from Scratch](notebooks/1.0-intro-llm-agents-from-scratch.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.0-intro-llm-agents-from-scratch.ipynb)

2. [Intro LLM Patterns and LangChain Components](notebooks/2.0-intro-llm-patterns-and-langchain-components.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/2.0-intro-llm-patterns-and-langchain-components.ipynb)

3. [Agents with LangChain & LangGraph](notebooks/3.0-agents-with-langchain-langgraph.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/3.0-agents-with-langchain-langgraph.ipynb)

4. [Intro to LangGraph](notebooks/4.0-intro-langgraph.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/4.0-intro-langgraph.ipynb)

5. [Local Research Agent with LangGraph](notebooks/5.0-local-research-agent-langgraph.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/5.0-local-research-agent-langgraph.ipynb)

6. [Local RAG Agent with LangGraph](notebooks/6.0-local-rag-agent-langgraph.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/6.0-local-rag-agent-langgraph.ipynb)

Additional resources can be found in:
- `notebooks/agent-deploy/` - Agent deployment examples
- `notebooks/assets-resources/` - Supporting assets and resources
- `notebooks/extra-notebooks/` - Additional example notebooks
- `notebooks/extra-scripts/` - Utility scripts and helpers
