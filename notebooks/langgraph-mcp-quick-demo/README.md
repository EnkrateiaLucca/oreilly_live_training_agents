# LangGraph MCP (Model Context Protocol) Quick Demo

This demo showcases how to connect MCP servers with LangGraph agents, allowing your agents to use tools exposed by external servers.

## What is MCP?

Model Context Protocol (MCP) is a standardized way to expose tools and capabilities from external servers to AI agents. With MCP, you can:
- Create modular tools that run in separate processes
- Expose APIs and services as agent tools
- Build reusable tool servers that work with any MCP-compatible framework

## Prerequisites

- Python 3.8+
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Project Structure

```
langgraph-mcp-quick-demo/
├── mcp_demo.py        # Main demo script
├── math_server.py     # MCP server for math operations
├── weather_server.py  # MCP server for weather info
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Running the Demo

### Step 1: Start the Weather Server

In a terminal, run:
```bash
python weather_server.py
```

This starts an HTTP server on port 8000 that exposes weather tools.

### Step 2: Run the Main Demo

In another terminal, run:
```bash
python mcp_demo.py
```

The demo will:
1. Connect to both MCP servers (math via stdio, weather via HTTP)
2. Create a LangGraph agent with the exposed tools
3. Run example queries demonstrating the agent using tools from both servers

## How It Works

1. **MCP Servers**: Each server defines tools using the `@mcp.tool()` decorator
   - `math_server.py`: Exposes `add` and `multiply` functions
   - `weather_server.py`: Exposes `get_weather` function

2. **MultiServerMCPClient**: Connects to multiple MCP servers with different transports
   - `stdio`: Direct process communication (math server)
   - `streamable_http`: HTTP-based communication (weather server)

3. **LangGraph Agent**: Uses `create_react_agent` to build an agent that can:
   - Understand when to use which tool
   - Call tools from different servers seamlessly
   - Combine results from multiple tools

## Example Outputs

The demo runs three examples:

1. **Math Calculation**: Uses the math server to compute `(3 + 5) x 12`
2. **Weather Query**: Uses the weather server to get weather for New York
3. **Combined Query**: Uses both servers to convert temperature from Fahrenheit to Celsius

## Extending the Demo

To add more MCP servers:

1. Create a new server file with `FastMCP`
2. Define tools using `@mcp.tool()` decorator
3. Add the server configuration to `MultiServerMCPClient`
4. The tools will automatically be available to the agent

## Troubleshooting

- **"Connection refused" error**: Make sure the weather server is running on port 8000
- **"File not found" error**: Update the path to `math_server.py` in `mcp_demo.py`
- **OpenAI errors**: Ensure your API key is set correctly

## Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [LangGraph MCP Integration Guide](https://langchain-ai.github.io/langgraph/agents/mcp/)