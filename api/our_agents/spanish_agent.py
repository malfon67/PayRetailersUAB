from agents import Agent

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

# Expose the agent instance for dynamic imports
agent_instance = spanish_agent