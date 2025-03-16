import asyncio
import requests
from agents import Agent, function_tool
from utils.perplexity_api import search_perplexity
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
from typing import Optional

class EnergyAgentOutput(BaseAgentOutput):
    """
    Output model for the Energy Agent.
    """
    country: Optional[str] = None
    tips: Optional[list[str]] = None

@function_tool
def get_renewable_energy_data(country: str) -> dict:
    """
    Fetch renewable energy data from IRENA and return it as JSON.
    
    Parameters:
    - country: Country name
    
    Returns:
    - Renewable energy data for the specified country in JSON format
    """
    print("Energy Agent is accessing IRENA API data. Country:", country)
    try:
        # Placeholder for IRENA API - actual endpoint may differ
        url = f"https://api.irena.org/api/v1/data?country={country}&technology=all&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "energy", "status": "success", "country": country, "data": data}
        else:
            return {"agent_type": "energy", "status": "error", "message": f"Error al acceder a los datos: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "energy", "status": "error", "message": f"Error en la consulta: {str(e)}"}

@function_tool
def get_energy_sustainability_tips() -> dict:
    """
    Provide tips on energy sustainability in JSON format.
    
    Returns:
    - Energy sustainability tips in JSON format
    """
    print("Energy Agent is providing sustainability tips.")
    tips = [
        "Instalar paneles solares para reducir la dependencia de la red eléctrica.",
        "Utilizar electrodomésticos de bajo consumo energético.",
        "Implementar sistemas de iluminación LED.",
        "Aislar adecuadamente la vivienda para reducir el uso de calefacción y aire acondicionado.",
        "Considerar alternativas de transporte sostenible como vehículos eléctricos o transporte público."
    ]
    return {"agent_type": "energy", "status": "success", "tips": tips}

@function_tool
def search_energy_info(query: str) -> dict:
    """
    Search for energy information using the Perplexity API.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print("Energy Agent is performing an internet search for energy information.")
    result = search_perplexity(query)
    print(result)
    return {"agent_type": "energy", "data": result}

energy_agent = Agent(
    name="Energy Agent",
    instructions=(
        BASE_STARTING_PROMPT +
        "Proporciona asistencia con temas de energía y sostenibilidad. Genera tu salida en formato JSON, y esta será transformada a HTML por el HTMLTransformer. "
        "Responde solo en español."
    ),
    tools=[get_renewable_energy_data, get_energy_sustainability_tips, search_energy_info],
    handoff_description="Provides energy and sustainability assistance.",
    output_type=EnergyAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = energy_agent
