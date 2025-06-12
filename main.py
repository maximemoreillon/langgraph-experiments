from langgraph.prebuilt import create_react_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_react_agent(
    model="openai:o3-mini", tools=[get_weather], prompt="You are a helpful assistant"
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response["messages"])
