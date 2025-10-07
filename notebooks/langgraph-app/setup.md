# LangGraph App Setup & Walkthrough

Complete tutorial for setting up and understanding your first LangGraph application.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Overview](#project-overview)
3. [Installation Steps](#installation-steps)
4. [Understanding the Code](#understanding-the-code)
5. [Running the Application](#running-the-application)
6. [Testing Your Agent](#testing-your-agent)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

### 1. Python 3.11 or Higher

Check your Python version:
```bash
python --version
# or
python3 --version
```

If you need to install/upgrade Python, visit [python.org](https://www.python.org/downloads/)

### 2. API Keys

You'll need two API keys:

#### A. LangSmith API Key (Free)
1. Go to [smith.langchain.com/settings](https://smith.langchain.com/settings)
2. Sign up for a free account
3. Navigate to "Settings" → "API Keys"
4. Create a new API key
5. Copy the key (starts with `lsv2_pt_`)

#### B. OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

> **Alternative**: You can use Anthropic's Claude instead. Get a key from [console.anthropic.com](https://console.anthropic.com/) and modify the code to use `ChatAnthropic` instead of `ChatOpenAI`.

---

## Project Overview

### What is LangGraph?

LangGraph is a framework for building stateful, multi-agent applications with LLMs. Key features:

- **Graphs**: Define your agent logic as nodes and edges
- **State**: Maintain conversation context and data
- **Persistence**: Save and resume conversations
- **Streaming**: Real-time response streaming
- **Human-in-the-loop**: Add approval steps

### Project Structure

```
langgraph-app/
├── src/
│   └── my_agent/
│       ├── __init__.py          # Makes my_agent a Python package
│       └── graph.py             # Main application logic
├── .env.example                 # Template for environment variables
├── .env                         # Your actual API keys (you'll create this)
├── langgraph.json              # Configuration for LangGraph Server
├── pyproject.toml              # Python project metadata and dependencies
├── README.md                   # Project overview
└── setup.md                    # This file!
```

---

## Installation Steps

### Step 1: Navigate to the Project

```bash
cd langgraph-app
```

### Step 2: Install LangGraph CLI

The CLI lets you run LangGraph apps locally.

```bash
pip install -U "langgraph-cli[inmem]"
```

Or if using `uv`:
```bash
uv pip install -U "langgraph-cli[inmem]"
```

### Step 3: Install Project Dependencies

Install the project in editable mode so your code changes are immediately reflected:

```bash
pip install -e .
```

This installs:
- `langgraph`: Core framework
- `langchain-openai`: OpenAI integration
- `langchain-anthropic`: Claude integration (optional)
- `langsmith`: Monitoring and tracing

### Step 4: Set Up Environment Variables

Create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your favorite text editor and add your API keys:

```bash
# .env
LANGSMITH_API_KEY=lsv2_pt_your_actual_key_here
OPENAI_API_KEY=sk-your_actual_key_here
```

> **Security Note**: Never commit `.env` files to version control!

---

## Understanding the Code

Let's walk through each file to understand how LangGraph works.

### 1. `langgraph.json` - Configuration

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/my_agent/graph.py:graph"
  },
  "env": ".env"
}
```

**What it does:**
- `dependencies`: Tells LangGraph to install the current directory as a package
- `graphs`: Maps the name "agent" to your graph object in `graph.py`
- `env`: Specifies where to find environment variables

### 2. `pyproject.toml` - Dependencies

This file defines your project metadata and dependencies using the standard Python packaging format.

**Key dependencies:**
- `langgraph>=0.2.60`: Core LangGraph framework
- `langchain-openai>=0.2.16`: OpenAI model integration
- `langsmith>=0.2.6`: Observability and monitoring

### 3. `src/my_agent/graph.py` - The Agent

This is where the magic happens! Let's break it down:

#### **State Definition**

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

- **State**: A TypedDict that defines what data flows through your graph
- **messages**: List of conversation messages
- **add_messages**: A reducer function that automatically merges new messages with existing ones

#### **LLM Initialization**

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
```

- Creates an OpenAI client
- `gpt-4o-mini`: Fast, cost-effective model
- `temperature=0.7`: Controls randomness (0 = deterministic, 1 = creative)

#### **Node Function**

```python
def chatbot_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

**What happens:**
1. Takes current state (with message history)
2. Sends all messages to the LLM
3. Returns LLM's response wrapped in a dict
4. LangGraph automatically merges this with existing state

#### **Graph Construction**

```python
def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    return graph_builder.compile()
```

**Graph structure:**
```
START → chatbot → END
```

This creates a simple linear flow:
1. Start
2. Execute chatbot node
3. End

**More complex graphs** can have:
- Multiple nodes
- Conditional edges (routing)
- Loops (iterative processing)
- Subgraphs

---

## Running the Application

### Local Development Server

Start the LangGraph development server:

```bash
langgraph dev
```

**Expected output:**
```
>    Ready!
>
>    - API: http://localhost:2024
>    - Docs: http://localhost:2024/docs
>    - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**What this does:**
- Starts a local API server on port 2024
- Enables hot-reloading (code changes auto-update)
- Uses in-memory storage (data doesn't persist between restarts)
- Provides OpenAPI documentation

### Using a Custom Port

```bash
langgraph dev --port 8000
```

### Using Safari?

Safari has issues connecting to localhost servers. Use the tunnel flag:

```bash
langgraph dev --tunnel
```

---

## Testing Your Agent

### Method 1: LangGraph Studio (Visual Interface)

1. Open the Studio URL from the `langgraph dev` output
2. Click "New Thread" to start a conversation
3. Type a message and press Enter
4. Watch the graph execute in real-time
5. See the state updates at each step

**Benefits:**
- Visual graph representation
- Step-by-step execution
- State inspection
- Time-travel debugging

### Method 2: Python SDK

Create a test script `test_agent.py`:

```python
from langgraph_sdk import get_client
import asyncio

async def main():
    # Connect to local server
    client = get_client(url="http://localhost:2024")

    # Stream responses
    async for chunk in client.runs.stream(
        None,  # Threadless run (no conversation persistence)
        "agent",  # Assistant name from langgraph.json
        input={
            "messages": [{
                "role": "user",
                "content": "What is LangGraph?",
            }],
        },
    ):
        print(f"Event: {chunk.event}")
        print(f"Data: {chunk.data}")
        print("-" * 50)

asyncio.run(main())
```

Run it:
```bash
python test_agent.py
```

### Method 3: REST API

Using `curl`:

```bash
curl -X POST "http://localhost:2024/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "messages": [{
        "role": "user",
        "content": "Hello!"
      }]
    }
  }'
```

### Method 4: Local Testing (No Server)

Test the graph directly in Python:

```bash
cd src/my_agent
python graph.py
```

This runs the `if __name__ == "__main__"` block in `graph.py`.

---

## Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'langgraph'`

**Solution:** Install dependencies
```bash
pip install -e .
```

### Problem: `AuthenticationError` from OpenAI

**Solution:** Check your `.env` file
1. Ensure `.env` exists in the project root
2. Verify your OpenAI API key is correct
3. Make sure there are no extra spaces or quotes

### Problem: Port 2024 already in use

**Solution:** Use a different port
```bash
langgraph dev --port 8000
```

### Problem: Can't connect to Studio in Safari

**Solution:** Use the tunnel flag
```bash
langgraph dev --tunnel
```

### Problem: Changes not reflecting

**Solution:** The dev server should auto-reload, but you can:
1. Stop the server (Ctrl+C)
2. Restart with `langgraph dev`

### Problem: `graph` not found in langgraph.json

**Solution:** Check your graph.py
1. Ensure `graph = create_graph()` exists at module level
2. Verify the path in `langgraph.json` is correct

---

## Next Steps

### 1. Add Memory/Persistence

Modify the graph to use a checkpointer:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
```

Now conversations persist!

### 2. Add Tools

Give your agent capabilities:

```python
from langchain_community.tools import DuckDuckGoSearchRun

tools = [DuckDuckGoSearchRun()]
llm_with_tools = llm.bind_tools(tools)
```

### 3. Add More Nodes

Create a multi-step workflow:

```python
graph_builder.add_node("researcher", research_node)
graph_builder.add_node("writer", writer_node)
graph_builder.add_edge("researcher", "writer")
```

### 4. Add Conditional Logic

Route based on content:

```python
def should_continue(state):
    if state["needs_approval"]:
        return "human_review"
    return "continue"

graph_builder.add_conditional_edges(
    "process",
    should_continue,
    {
        "human_review": "review_node",
        "continue": "next_node"
    }
)
```

### 5. Deploy to Production

When ready to deploy:

```bash
# Build for production
langgraph build

# Deploy to LangGraph Cloud
# Follow: https://langchain-ai.github.io/langgraph/cloud/
```

---

## Learning Resources

### Official Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/)
- [LangSmith Docs](https://docs.smith.langchain.com/)

### Tutorials
- [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [Build a ReAct Agent](https://langchain-ai.github.io/langgraph/tutorials/react-agent/)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)

### Examples
- [LangGraph Examples Repo](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [LangGraph Templates](https://github.com/langchain-ai/langgraph/tree/main/templates)

---

## Summary

You've learned:

✅ How to structure a LangGraph application
✅ Understanding State and message management
✅ Creating nodes and building graphs
✅ Running applications locally with `langgraph dev`
✅ Testing with Studio, SDK, and REST API
✅ Debugging and troubleshooting

**Key Takeaways:**
1. **State** flows through the graph and nodes update it
2. **Nodes** are functions that process state
3. **Edges** define the execution flow
4. **Reducers** (like `add_messages`) control how state updates merge

Now go build amazing agents! 🚀

---

## Questions?

- Check the [LangGraph Discord](https://discord.gg/langchain)
- Browse [GitHub Issues](https://github.com/langchain-ai/langgraph/issues)
- Read the [FAQ](https://langchain-ai.github.io/langgraph/faq/)

Happy coding! 🎉
