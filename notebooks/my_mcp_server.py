"""Demo MCP server for the LangGraph class — exposes three simple tools."""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("demo-server")

WEATHER_DB = {
    "lisbon": "22°C, sunny",
    "london": "14°C, cloudy",
    "new york": "18°C, partly cloudy",
    "tokyo": "25°C, humid",
    "paris": "16°C, rainy",
}

FACTS_DB = {
    "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs using a graph-based state machine.",
    "langchain": "LangChain is a framework for developing applications powered by large language models.",
    "mcp": "Model Context Protocol (MCP) is an open protocol that standardizes how applications expose tools and context to LLMs.",
    "react": "ReAct (Reasoning + Acting) is an agent pattern where the LLM alternates between reasoning steps and tool calls.",
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get the current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Lisbon'"}
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="calculate",
            description="Evaluate a simple arithmetic expression",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression, e.g. '42 * 7'",
                    }
                },
                "required": ["expression"],
            },
        ),
        Tool(
            name="lookup_fact",
            description="Look up a fact about an AI/ML topic (langgraph, langchain, mcp, react)",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic to look up"}
                },
                "required": ["topic"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        city = arguments["city"].lower()
        weather = WEATHER_DB.get(city, f"No data for '{arguments['city']}'")
        return [TextContent(type="text", text=f"Weather in {arguments['city']}: {weather}")]

    if name == "calculate":
        expr = arguments["expression"]
        try:
            result = eval(expr, {"__builtins__": {}})  # noqa: S307
            return [TextContent(type="text", text=f"{expr} = {result}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error evaluating '{expr}': {e}")]

    if name == "lookup_fact":
        topic = arguments["topic"].lower()
        fact = FACTS_DB.get(topic, f"No fact found for '{arguments['topic']}'")
        return [TextContent(type="text", text=fact)]

    raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
