"""
Weather MCP Server
==================

An MCP server that provides weather information as tools.
This server uses HTTP transport and can be accessed remotely.
"""

import asyncio
from mcp.server.fastmcp import FastMCP
import random

# Create MCP server instance
mcp = FastMCP("Weather")

# Mock weather data
WEATHER_DATA = {
    "New York": {"temp": 75, "condition": "Partly Cloudy", "humidity": 65},
    "Los Angeles": {"temp": 82, "condition": "Sunny", "humidity": 45},
    "Chicago": {"temp": 68, "condition": "Cloudy", "humidity": 70},
    "Houston": {"temp": 88, "condition": "Hot and Humid", "humidity": 80},
    "Phoenix": {"temp": 95, "condition": "Very Hot", "humidity": 20},
    "Philadelphia": {"temp": 73, "condition": "Clear", "humidity": 60},
    "San Antonio": {"temp": 85, "condition": "Warm", "humidity": 75},
    "San Diego": {"temp": 72, "condition": "Perfect", "humidity": 55},
    "Dallas": {"temp": 86, "condition": "Hot", "humidity": 65},
    "Boston": {"temp": 70, "condition": "Partly Cloudy", "humidity": 68},
}


@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get current weather information for a given location.
    
    Args:
        location: The city name to get weather for
        
    Returns:
        A string with weather information
    """
    # Normalize location name
    location_normalized = location.title()
    
    if location_normalized in WEATHER_DATA:
        data = WEATHER_DATA[location_normalized]
        return f"Weather in {location_normalized}: {data['temp']}°F, {data['condition']}, Humidity: {data['humidity']}%"
    else:
        # Return random weather for unknown locations
        temp = random.randint(60, 90)
        conditions = ["Sunny", "Cloudy", "Partly Cloudy", "Clear"]
        condition = random.choice(conditions)
        humidity = random.randint(40, 80)
        return f"Weather in {location}: {temp}°F, {condition}, Humidity: {humidity}%"


@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for a location.
    
    Args:
        location: The city name
        days: Number of days to forecast (1-7)
        
    Returns:
        A string with forecast information
    """
    if days < 1 or days > 7:
        return "Please specify days between 1 and 7"
    
    forecast = f"Forecast for {location} for next {days} days:\n"
    
    for day in range(1, days + 1):
        temp_high = random.randint(65, 95)
        temp_low = temp_high - random.randint(10, 20)
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Chance of Rain", "Clear"]
        condition = random.choice(conditions)
        forecast += f"Day {day}: High {temp_high}°F, Low {temp_low}°F, {condition}\n"
    
    return forecast.strip()


if __name__ == "__main__":
    print("Starting Weather MCP Server on port 8000...")
    print("Server will be available at http://localhost:8000/mcp")
    # Run with HTTP transport on port 8000
    mcp.run(transport="streamable-http", port=8000)