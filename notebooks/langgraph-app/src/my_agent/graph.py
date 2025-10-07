"""
Simple LangGraph Agent Example

This module demonstrates a basic LangGraph application with:
- A single agent node that processes messages
- State management for conversation history
- Integration with OpenAI's GPT models
"""

from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# Define the state structure
class State(TypedDict):
    """
    State represents the data structure that flows through the graph.

    Attributes:
        messages: List of conversation messages with automatic merging behavior
    """
    messages: Annotated[list, add_messages]


# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


def chatbot_node(state: State) -> dict:
    """
    Main chatbot node that processes incoming messages.

    This function:
    1. Takes the current state with message history
    2. Sends messages to the LLM
    3. Returns the LLM's response to be added to the state

    Args:
        state: Current state containing message history

    Returns:
        Dictionary with the new message to add to state
    """
    # Invoke the LLM with the message history
    response = llm.invoke(state["messages"])

    # Return the response message to be added to state
    return {"messages": [response]}


# Build the graph
def create_graph():
    """
    Creates and compiles the LangGraph application.

    The graph structure:
    START -> chatbot_node -> END

    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize graph builder
    graph_builder = StateGraph(State)

    # Add the chatbot node
    graph_builder.add_node("chatbot", chatbot_node)

    # Define edges: START -> chatbot -> END
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    # Compile the graph
    return graph_builder.compile()


# Create the graph instance (required by langgraph.json)
graph = create_graph()


# For local testing
if __name__ == "__main__":
    # Example: Test the graph locally
    from pprint import pprint

    # Test input
    test_input = {
        "messages": [
            {"role": "user", "content": "Hello! What is LangGraph?"}
        ]
    }

    # Run the graph
    print("Testing the graph locally...")
    result = graph.invoke(test_input)

    print("\nConversation:")
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")
