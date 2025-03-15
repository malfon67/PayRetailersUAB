from agents import Agent

emigration_agent = Agent(
    name="Emigration Agent",
    instructions="You provide assistance with emigration-related topics. Respond only in Spanish.",
)

# Expose the agent instance for dynamic imports
agent_instance = emigration_agent