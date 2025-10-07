"""
LangGraph MCP (Model Context Protocol) Demo
===========================================

This demo shows how to connect MCP servers with LangGraph agents.
MCP allows you to expose tools from external servers to your agents.
"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI


async def main():
    """
    Main function demonstrating LangGraph MCP integration.
    """
    
    # Initialize MCP client with multiple servers
    # We'll connect to both a math server (stdio) and weather server (HTTP)
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full path to your math_server.py
                "args": ["./math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # Ensure the weather server is running on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    
    # Get tools from all connected MCP servers
    tools = await client.get_tools()
    
    print(f"Connected to MCP servers. Available tools: {[tool.name for tool in tools]}")
    
    # Create a React agent with the MCP tools
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4.1", temperature=0),
        tools
    )
    
    # Example 1: Math calculation
    print("\n=== Example 1: Math Calculation ===")
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What's (3 + 5) x 12?"}]}
    )
    print(f"Response: {math_response['messages'][-1].content}")
    
    # Example 2: Weather query
    print("\n=== Example 2: Weather Query ===")
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the weather in New York?"}]}
    )
    print(f"Response: {weather_response['messages'][-1].content}")
    
    # Example 3: Combined query
    print("\n=== Example 3: Combined Query ===")
    combined_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "If the temperature in NYC is 75°F, what is that in Celsius? Calculate (75-32) x 5/9"}]}
    )
    print(f"Response: {combined_response['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(main())