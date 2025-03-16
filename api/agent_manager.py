import os
import importlib
import re
from groq import Groq
from openai import AsyncAzureOpenAI
from agents import Agent, set_default_openai_client, Runner, OpenAIChatCompletionsModel
from our_agents_definition.base_agent import BaseAgentOutput
from supervisor import Supervisor
from settings import load_prompt, SUPERVISOR_PROMPT_FILE  # Import the new load_prompt function
from dotenv import load_dotenv
import json  # Added import for JSON formatting
from openai import AzureOpenAI
from transformers.html_transformer  import HTMLTransformer  # Import HTMLTransformer

# Load environment variables
load_dotenv()

llm_model_name = os.getenv("GPT4O_MINI_DEPLOYMENT")

# Create OpenAI client using Azure OpenAI
openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=llm_model_name
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
  azure_deployment=llm_model_name
)

# Set up Groq client
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"))

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client, False)

azure_model = OpenAIChatCompletionsModel(
    model=llm_model_name,
    openai_client=openai_client,
)

# Instantiate HTMLTransformer
html_transformer = HTMLTransformer(groq_client, llm_model_name)

# Dynamically import all agents from the agents folder
agents = []
agents_folder = os.path.join(os.path.dirname(__file__), "our_agents")
if not os.path.isdir(agents_folder):
    raise FileNotFoundError(f"Agents folder not found: {agents_folder}")
for filename in os.listdir(agents_folder):
    if filename.endswith("_agent.py"):
        module_name = f"our_agents.{filename[:-3]}"
        module = importlib.import_module(module_name)
        print(f"Loaded module: {module_name}")
        # Access the exposed agent_instance directly
        agent_instance = getattr(module, "agent_instance", None)
        if agent_instance:
            # Dynamically set the model and HTMLTransformer for the agent
            agent_instance.model = azure_model
            agent_instance.html_transformer = html_transformer
            agents.append(agent_instance)

# Print the names of the loaded agents
print(f"Loaded {len(agents)} agents:")
for agent in agents:
    print(f"- {agent.name}")



# Load the customizable supervisor prompt from the plain text file
supervisor_prompt = load_prompt(SUPERVISOR_PROMPT_FILE, "This agent provides assistance with general queries.")

# Combine the settings prompt with agent instructions in a policy-compliant way
agent_instructions = "Directrices para la conversación:\n"
agent_instructions += "1. Comunícate en español.\n"
agent_instructions += "2. Ayuda a identificar las necesidades del usuario.\n"
agent_instructions += "3. Utiliza los recursos disponibles para ofrecer soluciones apropiadas.\n"
agent_instructions += f"4. Recursos especializados disponibles ({len(agents)}):\n"

# Add information about each available agent in a neutral way
for agent in agents:
    agent_instructions += f"   - {agent.name}: Para consultas relevantes.\n"

if supervisor_prompt:
    supervisor_prompt += "\n\n" + agent_instructions
else:
    supervisor_prompt = agent_instructions

print("Supervisor prompt updated with guidelines")

# Update supervisor to include specialized agents, the loaded prompt, and the HTMLTransformer
supervisor_agent = Supervisor(
    agents=agents,
    model=azure_model,
    prompt=supervisor_prompt,
    html_transformer=html_transformer
)

# Store conversation history and pain points in memory (can be replaced with a database for persistence)
conversation_histories = {}
user_data = {}  # Placeholder for user data
user_pain_points = {}  # Store pain points for each user
user_good_points = {}  # Store good points for each user

from pydantic import BaseModel

async def extract_points_from_response(user_input: str) -> list:
    """
    Extract specific problems mentioned by the user from the LLM response in JSON format by sending a structured prompt.
    
    Parameters:
    - supervisor_agent: The supervisor agent instance
    - user_input: The user's input message
    
    Returns:
    - A list of specific problems extracted from the JSON response
    """

    class PointsResponse(BaseModel):
        pain_points: list[str]
        good_points: list[str]


    structured_prompt = f"""
    {user_input}
    
    Por favor, analiza este mensaje y detecta problemas específicos mencionados por el usuario y puntos positivos específicos mencionados por el usuario.
    Por ejemplo:
    - "Tengo problemas para pagar mis facturas" se traduce a "problema": "problemas financieros"
    - "Estoy preocupado por mi salud"   se traduce a "problema": "preocupaciones de salud"
    - "No puedo encontrar trabajo"    se traduce a "problema": "desafíos laborales"
    - "Estoy contento con el servicio" se traduce a "punto positivo": "satisfacción con el servicio"
    - "Me gusta la atención al cliente" se traduce a "punto positivo": "atención al cliente"
    - "Me encuentro con salud y bienestar" se traduce a "punto positivo": "salud y bienestar"
    Solo se requiere un problema por mensaje.
    """
    try:
        completion = client.beta.chat.completions.parse(
            model=llm_model_name,
            messages=[
                {"role": "system", "content": structured_prompt}
            ],
            response_format=PointsResponse
        )
        response = completion.choices[0].message.parsed

        print(f"Pain point response: {response.pain_points}")
        print(f"Good point response: {response.good_points}")
 
        return response
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing pain points response: {e}")
        return []  # Fallback if the response is not valid JSON or processing fails

async def handle_conversation(payload: dict) -> dict:
    """
    Handles the conversation flow based on the provided JSON schema.
    Ensures conversation history is formatted properly for the LLM.
    """
    payload_type = payload.get("type")
    user_id = payload.get("user_id")  # Unique identifier for the user
    if not user_id:
        return {"error": "User ID is required", "status_code": 400}

    # Initialize conversation history and pain points for the user if not already present
    if user_id not in conversation_histories:
        conversation_histories[user_id] = []
    if user_id not in user_pain_points:
        user_pain_points[user_id] = []
    if user_id not in user_good_points:
        user_good_points[user_id] = []

    # Handle the start of the conversation
    if payload_type == "start":
        user_data_for_user = payload.get("user_data", {})  # Use a local variable to avoid shadowing the global dictionary
        
        # Format the user data as JSON, but avoid potential policy triggers
        formatted_user_data = json.dumps(user_data_for_user, indent=2, ensure_ascii=False)
        user_context = f"Información de usuario:\n```json\n{formatted_user_data}\n```\n"
        user_context += "Inicia una conversación amable en español con esta persona. "
        user_context += "Pregunta sobre cómo puedes ayudarle hoy. No utilices ningún agente especializado."
        user_context += "Simplemente comienza la conversación y deja que el sistema maneje el resto."

        try:
            # Process the user context through the supervisor
            # result = await supervisor_agent.process_input(user_context)

            result = client.chat.completions.create(
                model=llm_model_name,
                messages=[
                    {"role": "system", "content": user_context}
                ]
            )

            output = result.choices[0].message.content

            print(f"Initial conversation output: {output}")

            # Store conversation for future reference
            conversation_histories[user_id].append({"content": user_context, "role": "user"})
            conversation_histories[user_id].append({"content": output, "role": "assistant"})
            
            return {
                "type": "response",
                "user_id": user_id,
                "data": BaseAgentOutput(agent_type="html", status="success", data=output),
                "pain_points": [],  # No pain points extracted at this stage
                "good_points": [],  # No good points extracted at this stage
                "last_agent": None  # No specialized agent used at this stage
            }
        except Exception as e:
            print(f"Error processing initial conversation: {str(e)}")
            # Provide a safe fallback response
            fallback_response = "Hola, ¿en qué puedo ayudarte hoy?"
            
            conversation_histories[user_id].append({"content": user_context, "role": "user"})
            conversation_histories[user_id].append({"content": fallback_response, "role": "assistant"})
            
            return {
                "type": "response",
                "user_id": user_id,
                "data": BaseAgentOutput(agent_type="html", status="success", data=fallback_response),
                "pain_points": [],
                "good_points": [],
                "last_agent": None
            } 

    # Handle sequential prompts
    elif payload_type == "prompt":
        prompt_text = payload.get("data", "")
        if not prompt_text:
            return {"error": "Prompt text is required for type 'prompt'", "status_code": 400}

        # Retrieve user data for the user
        user_data_for_user = user_data.get(user_id, {})
        formatted_user_data = json.dumps(user_data_for_user, indent=2, ensure_ascii=False)
        user_context = f"Información de usuario:\n```json\n{formatted_user_data}\n```\n"

        # Append user data to the prompt text
        prompt_text = user_context + prompt_text

        try:
            # Extract pain points using the new function
            points = await extract_points_from_response(prompt_text)

            new_pain_points = [point.capitalize() for point in points.pain_points]
            new_good_points = [point.capitalize() for point in points.good_points]

            print(f"Extracted pain points: {new_pain_points} from user_id: {user_id}")
            
            # Append new pain points to the user's existing pain points
            user_pain_points[user_id].extend(new_pain_points)
            user_pain_points[user_id] = list(set(user_pain_points[user_id]))  # Ensure uniqueness

            # Append new good points to the user's existing good points
            user_good_points[user_id].extend(new_good_points)
            user_good_points[user_id] = list(set(user_good_points[user_id]))  # Ensure uniqueness
            
            # Process the user input through the supervisor agent
            html_output = await supervisor_agent.process_input(prompt_text)

            # Extract the dynamically generated HTML from the agent's response
            # html_output = result.final_output  # Assuming the agent returns HTML in final_output

            # Store conversation for future reference
            conversation_histories[user_id].append({"content": prompt_text, "role": "user"})
            conversation_histories[user_id].append({"content": html_output, "role": "assistant"})

            return {
                "type": "response",
                "user_id": user_id,
                "data": html_output,  # Return the HTML output directly
                "pain_points": user_pain_points[user_id],
                "good_points": user_good_points[user_id],
                # "last_agent": result.last_agent.name
            } 
        except Exception as e:
            print(f"Error processing prompt: {str(e)}")
            print(f"User ID: {user_id}")
            print(f"Prompt text: {prompt_text}")
            print(f"Conversation history: {conversation_histories.get(user_id, [])}")
            # Provide a safe fallback response
            fallback_response = "Entiendo. ¿Hay algo más en lo que pueda ayudarte?"
            conversation_histories[user_id].append({"content": prompt_text, "role": "user"})
            conversation_histories[user_id].append({"content": fallback_response, "role": "assistant"})
            
            return {
                "type": "response",
                "user_id": user_id,
                "data": BaseAgentOutput(agent_type="html", status="success", data=fallback_response),
                "pain_points": user_pain_points[user_id],
                "good_points": user_good_points[user_id],
                "last_agent": supervisor_agent.main_assistant.name
            }

    # Handle the end of the conversation
    elif payload_type == "stop":
        # Generate a final report based on all previous conversation
        
        # Create a formatted string from the conversation history
        conversation_text = ""
        for entry in conversation_histories.get(user_id, []):
            role = entry.get("role", "system")
            content = entry.get("content", "")
            conversation_text += f"{role.capitalize()}: {content}\n\n"
        
        try:
            # Ensure user_data is initialized for the user
            user_data_for_user = user_data.get(user_id, {})

            # Find the Final Output Agent in the list of agents
            final_output_agent = None
            for agent in agents:
                if "Final Output Agent" in agent.name:
                    final_output_agent = agent
                    break
            
            # If we found the Final Output Agent, use it directly
            if final_output_agent:
                print(f"Using agent: {final_output_agent.name} for final summary")
                
                # Prepare structured input for the Final Output Agent
                final_input = {
                    "conversation": conversation_text,
                    "user_data": json.dumps(user_data_for_user, ensure_ascii=False),
                    "pain_points": user_pain_points.get(user_id, []),
                    "good_points": user_good_points.get(user_id, [])
                }
                
                # Format input for the Final Output Agent
                formatted_input = [{"content": json.dumps(final_input), "role": "user"}]
                result = await Runner.run(final_output_agent, input=formatted_input)
                
                final_output = html_transformer.transform_to_html(result.final_output)
                
                # Clean up conversation history
                conversation_histories.pop(user_id, None)
                
                return {
                    "type": "final_response", 
                    "data": final_output,
                    "pain_points": user_pain_points.pop(user_id, []),
                    "good_points": user_good_points.pop(user_id, []),
                    "last_agent": final_output_agent.name
                }
            else:
                # Fall back to the supervisor if the Final Output Agent isn't found
                print("Final Output Agent not found, using supervisor agent instead")
                final_output = await supervisor_agent.process_input(conversation_text)
                # final_output = result.final_output
                
                # Clean up conversation history
                conversation_histories.pop(user_id, None)
                
                return {
                    "type": "response",
                    "data": BaseAgentOutput(agent_type="html", status="success", data=final_output),
                    "pain_points": user_pain_points.pop(user_id, []),
                    "good_points": user_good_points.pop(user_id, []),
                    "last_agent": supervisor_agent.main_assistant.name
                }
                
        except Exception as e:
            print(f"Error processing final summary: {str(e)}")
            # Provide a safe fallback response
            fallback_response = "Gracias por tu consulta. Si necesitas más ayuda, no dudes en contactarnos nuevamente."
            conversation_histories.pop(user_id, None)
            return {
                "type": "response",
                "data": fallback_response,
                "pain_points": user_pain_points.pop(user_id, []),
                "good_points": user_good_points.pop(user_id, [])
            }

    # Handle invalid types
    else:
        return {"error": "Invalid type in payload", "status_code": 400}