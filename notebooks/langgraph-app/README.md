# My LangGraph Agent Tutorial

A simple, educational LangGraph application demonstrating the basics of building AI agents.

## 📚 What You'll Learn

This tutorial project teaches you:

- **LangGraph Basics**: Understanding nodes, edges, and state management
- **Agent Architecture**: Building a simple conversational AI agent
- **Local Development**: Running and testing LangGraph apps locally
- **API Integration**: Using the LangGraph Server and SDK
- **State Management**: Managing conversation history across interactions

## 🏗️ Project Structure

```
langgraph-app/
├── src/
│   └── my_agent/
│       ├── __init__.py       # Package initialization
│       └── graph.py          # Main agent graph definition
├── .env.example              # Environment variables template
├── langgraph.json           # LangGraph configuration
├── pyproject.toml           # Project dependencies
├── README.md                # This file
└── setup.md                 # Complete setup walkthrough
```

## 🎯 What This Agent Does

This simple agent:
1. Receives messages from users
2. Processes them using OpenAI's GPT models
3. Maintains conversation context
4. Returns intelligent responses

## 🚀 Quick Start

See [setup.md](setup.md) for complete setup instructions.

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- LangSmith API key (free)

### Installation

```bash
# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the server
langgraph dev
```

## 🔑 Key Concepts

### State Management
The agent uses a `State` TypedDict with an `add_messages` reducer to automatically merge new messages into the conversation history.

### Graph Structure
```
START → chatbot_node → END
```

Simple linear flow: receive message → process with LLM → return response

### Node Function
Each node is a Python function that:
- Takes current state as input
- Performs operations
- Returns updates to the state

## 📖 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)

## 🎓 Educational Use

This project is designed for teaching and learning. Feel free to:
- Modify the code
- Add new features
- Experiment with different models
- Add more nodes and edges
- Implement tools and capabilities

## 📝 Next Steps

After completing this tutorial, try:
1. Adding tool calling capabilities
2. Implementing memory persistence
3. Creating multi-node workflows
4. Adding human-in-the-loop interactions
5. Deploying to production

## 🤝 Contributing

This is a tutorial project. Students are encouraged to fork and customize!
