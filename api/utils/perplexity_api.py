import os
from openai import OpenAI

def search_perplexity(query: str) -> dict:
    """
    Perform a search using the Perplexity API via OpenAI client.
    
    Parameters:
    - query: The search query
    
    Returns:
    - Search results in JSON format
    """
    print(f"Performing Perplexity API search for query: {query}")
    try:
        # Initialize the OpenAI client
        client = OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            base_url="https://api.perplexity.ai"
        )
        
        # Prepare the messages for the chat completion
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you need to "
                    "engage in a helpful, detailed, polite conversation with a user."
                ),
            },
            {   
                "role": "user",
                "content": query,
            },
        ]
        
        # Perform the chat completion
        response = client.chat.completions.create(
            model="sonar",
            messages=messages,
        )

        # print(response)
        
        # return {"status": "success", "query": query, "results": response}
        return response.choices[0].message.content
    except Exception as e:
        return {"status": "error", "message": f"Error in search: {str(e)}"}
