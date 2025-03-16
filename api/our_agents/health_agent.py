from agents import Agent, function_tool
from utils.perplexity_api import search_perplexity
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
# from typing import Optional

class HealthAgentOutput(BaseAgentOutput):
    """
    Output model for the Health Agent.
    """
    # country_code: Optional[str] = None
    # value: Optional[str] = None

@function_tool
def search_health_info(query: str) -> dict:
    """
    Search for health information using the Perplexity API.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print("Health Agent is performing an internet search for health information.")
    result = search_perplexity(query)
    return {"agent_type": "health", "data": result}



health_agent = Agent(
    name="Health Agent",
    instructions=(
        BASE_STARTING_PROMPT +
        "Proporciona asistencia con temas relacionados con la salud. Genera tu salida en formato JSON, y esta será transformada a HTML por el HTMLTransformer. "
        "Responde solo en español."
    ),
    tools=[search_health_info],
    handoff_description="Provides health-related assistance. Accesses WHO data and performs web searches for health information. Only use it if user mentions something related to health.",
    output_type=HealthAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = health_agent
