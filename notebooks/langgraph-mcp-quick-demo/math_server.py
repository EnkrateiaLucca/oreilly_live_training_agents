"""
Math MCP Server
===============

A simple MCP server that exposes mathematical operations as tools.
This server uses stdio transport for local communication.
"""

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers. Returns a float result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


if __name__ == "__main__":
    # Run the server using stdio transport
    print("Starting Math MCP Server...")
    mcp.run(transport="stdio")