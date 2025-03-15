import asyncio
import requests
from agents import Agent, function_tool
import os
from utils.perplexity_api import search_perplexity

@function_tool
def get_climate_data(lat: float, lon: float) -> dict:
    """
    Fetch climate data from NASA Earth Data API and return it as JSON.
    
    Parameters:
    - lat: Latitude
    - lon: Longitude
    
    Returns:
    - Climate data in JSON format
    """
    print("Climate Agent is accessing NASA Earth Data API.")
    try:
        url = f"https://api.nasa.gov/earth/temperature?lat={lat}&lon={lon}&api_key=LTty4H8UrdDVS1JeMtTijWxcWRS2QVChpQddl7hN"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "climate", "status": "success", "latitude": lat, "longitude": lon, "data": data}
        else:
            return {"agent_type": "climate", "status": "error", "message": f"Error al acceder a los datos: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "climate", "status": "error", "message": f"Error en la consulta: {str(e)}"}

@function_tool
def get_environmental_risk(country: str) -> dict:
    """
    Provide information about environmental risks in a specific country in JSON format.
    
    Parameters:
    - country: Country name
    
    Returns:
    - Environmental risk information in JSON format
    """
    print("Climate Agent is providing environmental risk information.")
    environmental_risks = {
        "mexico": "México enfrenta riesgos de sequías, huracanes y aumento del nivel del mar.",
        "brazil": "Brasil enfrenta riesgos de deforestación, inundaciones y sequías.",
        "colombia": "Colombia enfrenta riesgos de deslizamientos de tierra, inundaciones y sequías.",
        "argentina": "Argentina enfrenta riesgos de sequías e inundaciones."
    }
    
    country_lower = country.lower()
    if country_lower in environmental_risks:
        return {"agent_type": "climate", "status": "success", "country": country, "risk": environmental_risks[country_lower]}
    else:
        return {"agent_type": "climate", "status": "error", "message": f"No hay información específica sobre riesgos ambientales para {country}."}

@function_tool
def search_climate_info(query: str) -> dict:
    """
    Search for climate information using the Perplexity API.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print("Climate Agent is performing an internet search for climate information.")
    result = search_perplexity(query)
    return {"agent_type": "climate", **result}

climate_agent = Agent(
    name="Climate Agent",
    instructions="You provide assistance with climate and environmental topics. You can access NASA Earth Data for climate information and search the web for climate-related queries. Respond only in Spanish.",
    tools=[get_climate_data, get_environmental_risk, search_climate_info],
    handoff_description="Provides climate and environmental information, can access NASA Earth data and search the web for climate-related information. Use for questions about climate change, weather patterns, or environmental risks."
)

# Expose the agent instance for dynamic imports
agent_instance = climate_agent
