import asyncio
import requests
from agents import Agent, function_tool
from utils.perplexity_api import search_perplexity
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
from typing import Optional

class HealthAgentOutput(BaseAgentOutput):
    """
    Output model for the Health Agent.
    """
    country_code: Optional[str] = None
    indicator: Optional[str] = None
    value: Optional[str] = None

@function_tool
def get_who_health_data(country_code: str, indicator: str) -> dict:
    """
    Fetch health data from WHO API and return it as JSON.
    
    Parameters:
    - country_code: ISO 3166-1 alpha-2 country code
    - indicator: WHO indicator code
    
    Returns:
    - Health data in JSON format
    """
    print("Health Agent is accessing WHO API data.")
    try:
        url = f"https://ghoapi.azureedge.net/api/{indicator}/country/{country_code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "health", "status": "success", "country_code": country_code, "indicator": indicator, "value": data.get('value')}
        else:
            return {"agent_type": "health", "status": "error", "message": f"Error al acceder a los datos: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "health", "status": "error", "message": f"Error en la consulta: {str(e)}"}

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
        "Proporciona asistencia con temas relacionados con la salud. Puedes acceder a datos de la OMS y buscar información de salud en la web. Responde solo en español."
    ),
    tools=[get_who_health_data, search_health_info],
    handoff_description="Provides health-related assistance.",
    output_type=HealthAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = health_agent
