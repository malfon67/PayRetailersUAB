from agents import Agent, function_tool
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
from utils.perplexity_api import search_perplexity

class EmigrationAgentOutput(BaseAgentOutput):
    """
    Output model for the Emigration Agent.
    """
    # response: Optional[str] = None
    # additional_info: Optional[str] = None

@function_tool
def search_emigration_info(query: str) -> dict:
    """
    Search for emigration-related information using the Perplexity API.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print("Emigration Agent is performing an internet search for emigration-related information.")
    result = search_perplexity(query)
    return {"agent_type": "emigration", "data": result}

emigration_agent = Agent(
    name="Emigration Agent",
    instructions=(
        BASE_STARTING_PROMPT +
        "Proporciona asistencia con temas relacionados con la emigración. Responde solo en español."
    ),
    tools=[search_emigration_info],
    handoff_description="Provides assistance with emigration-related topics.",
    output_type=EmigrationAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = emigration_agent