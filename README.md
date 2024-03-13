# O'Reilly Live Trainining - Getting Started with LLM Agents using LangChain

## Setup

**Conda**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.10.
- Create an environment: `conda create -n oreilly-agents python=3.10`
- Activate your environment with: `conda activate oreilly-agents`
- Install requirements with: `pip install -r requirements.txt`
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
    pip install -r requirements.txt
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

1. [Intro Agents](notebooks/1.0-intro-agents.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.0-intro-agents.ipynb)

2. [Intro Agents OpenAI Functions](notebooks/1.1-intro-agents-openai-functions.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.1-intro-agents-openai-functions.ipynb)

3. [Intro LangChain](notebooks/1.2-intro-langchain.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/1.2-intro-langchain.ipynb)

4. [Building LLM Agents with LangChain](notebooks/2.0-building-llm-agents-with-langchain.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/2.0-building-llm-agents-with-langchain.ipynb)

5. [Building Agents with LangChain and LCEL Interface](notebooks/2.1-building-agents-with-langchain-and-LCEL-interface.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/2.1-building-agents-with-langchain-and-LCEL-interface.ipynb)

6. [LangChain GitHub Agent Prototype](notebooks/3.0-langchain-github-agent-prototype.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/3.0-langchain-github-agent-prototype.ipynb)

7. [Building a Simple Research Agent](notebooks/4.0-building-a-simple-research-agent.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/4.0-building-a-simple-research-agent.ipynb)

8. [LangChain Deploy Chat with Website](notebooks/5.0-langchain-deploy-chat-with-website.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/5.0-langchain-deploy-chat-with-website.ipynb)

9. [LangChain Deploy Agent](notebooks/5.1-langchain-deploy-agent.ipynb)
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/5.1-langchain-deploy-agent.ipynb)

10. [Jira Issues Exploring](notebooks/jira_issues_exploring.ipynb)
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_agents/blob/main/notebooks/jira_issues_exploring.ipynb)

