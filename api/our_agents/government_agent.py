from agents import Agent, function_tool
from utils.perplexity_api import search_perplexity

@function_tool
def get_government_info(country: str, city: str, query: str) -> dict:
    """
    Search for government-related information using the Perplexity API.
    
    Parameters:
    - country: The user's country
    - city: The user's city
    - query: The specific question or topic
    
    Returns:
    - Search results in JSON format
    """
    print(f"Government Agent is searching for information about {query} in {city}, {country}.")
    full_query = f"{query} in {city}, {country} (laws, government processes, or related information)"
    result = search_perplexity(full_query)
    return {"agent_type": "government", "country": country, "city": city, **result}

government_agent = Agent(
    name="Government Agent",
    instructions=(
        "You provide assistance with questions related to laws, government processes, "
        "and other government-related topics. You can search the web for information "
        "specific to the user's country and city. Respond only in Spanish."
    ),
    tools=[get_government_info],
    handoff_description=(
        "Provides assistance with laws, government processes, and other government-related topics. "
        "Can search the web for information specific to the user's country and city. Use for questions "
        "about legal processes, government services, or regulations."
    )
)

# Expose the agent instance for dynamic imports
agent_instance = government_agent
