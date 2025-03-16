import asyncio
import requests
from agents import Agent, function_tool
from utils.perplexity_api import search_perplexity
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
from typing import Optional

class MoneyAgentOutput(BaseAgentOutput):
    """
    Output model for the Money Agent.
    """
    # topic: Optional[str] = None
    # advice: Optional[str] = None
    # value: Optional[float] = None

@function_tool
def get_financial_advice(topic: str) -> dict:
    """
    Provide financial advice based on the topic in JSON format.
    
    Parameters:
    - topic: Financial topic
    
    Returns:
    - Financial advice in JSON format
    """
    print("Money Agent is providing financial advice.")
    advice = f"Para el tema '{topic}', se recomienda mantener un presupuesto equilibrado y consultar con un asesor financiero."
    return {"agent_type": "money", "status": "success", "topic": topic, "advice": advice}

@function_tool
def get_world_bank_data(country_code: str, indicator: str) -> dict:
    """
    Fetch economic data from World Bank API and return it as JSON.
    
    Parameters:
    - country_code: ISO 3166-1 alpha-3 country code
    - indicator: World Bank indicator code
    
    Returns:
    - Economic data in JSON format
    """
    print("Money Agent is accessing World Bank API data.")
    try:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and len(data[1]) > 0:
                return {"agent_type": "money", "status": "success", "country_code": country_code, "indicator": indicator, "value": data[1][0]['value']}
            else:
                return {"agent_type": "money", "status": "error", "message": "No se encontraron datos para el indicador solicitado."}
        else:
            return {"agent_type": "money", "status": "error", "message": f"Error al acceder a los datos: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "money", "status": "error", "message": f"Error en la consulta: {str(e)}"}

@function_tool
def get_eclac_data(country_code: str, topic: str) -> dict:
    """
    Fetch socioeconomic data from the Economic Commission for Latin America and the Caribbean (ECLAC).
    
    Parameters:
    - country_code: Country code
    - topic: Topic of interest (e.g., 'poverty', 'education', 'employment')
    
    Returns:
    - ECLAC data for the specified parameters in JSON format
    """
    print("Money Agent is accessing ECLAC API data.")
    try:
        # This is a placeholder since direct API access might require specific endpoints
        url = f"https://statistics.cepal.org/portal/cepalstat/api/v1/indicator?country={country_code}&topic={topic}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "money", "status": "success", "country_code": country_code, "topic": topic, "data": data}
        else:
            return {"agent_type": "money", "status": "error", "message": f"Error al acceder a los datos de CEPAL: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "money", "status": "error", "message": f"Error en la consulta a la API de CEPAL: {str(e)}"}

@function_tool
def search_financial_info(query: str) -> dict:
    """
    Search for financial information using the Perplexity API.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print("Money Agent is performing an internet search for financial information.")
    result = search_perplexity(query)
    return {"agent_type": "money", "data": result}


money_agent = Agent(
    name="Money Agent",
    instructions=(
        BASE_STARTING_PROMPT +
        "Proporciona asistencia con temas financieros y bancarios. Puedes acceder a datos del Banco Mundial y buscar información financiera en la web. Responde solo en español."
    ),
    tools=[search_financial_info],
    handoff_description="Provides financial and banking assistance.",
    output_type=MoneyAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = money_agent
