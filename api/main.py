from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from typing import Union
import io
from agent_manager import supervisor_agent, handle_conversation  # Import supervisor_agent and handle_conversation
from settings import get_settings_ui, update_settings  # Import settings functions
import random
import uuid

from agents import RawResponsesStreamEvent
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
from html_templates import generate_html_from_json  # Import the HTML templates module

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    # Add any other domains that need access here
    "*",  # Allow all origins (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Placeholder function for audio transcription
def transcribe_audio(audio_file: io.BytesIO) -> str:
    # Replace this with actual transcription logic (e.g., using a library like SpeechRecognition or Whisper)
    return "Transcribed text from audio"

# Function to get LLM agent response
async def get_llm_response(input_text: str) -> str:
    # Use the supervisor_agent to process the input text
    result = await supervisor_agent.process_input(input_text)
    return result.final_output


@app.post("/process-input/")
async def process_input(payload: dict = Body(...)):
    """
    Handles the conversation flow based on the provided JSON schema.
    """
    response = await handle_conversation(payload)

    # Handle errors returned by the conversation handler
    if "error" in response:
        return JSONResponse(content={"error": response["error"]}, status_code=response.get("status_code", 400))

    # Check if the response is from the main agent and set agent_type to "main"
    if "agent_type" not in response:
        response["agent_type"] = "main"

    # Generate HTML output using the html_templates module
    html_output = generate_html_from_json(response)

    # Return both raw data and HTML data
    return {
        "type": response.get("type"),
        "user_id": payload.get("user_id"),
        "data": response.get("data"),
        "html_data": html_output,
        "pain_points": response.get("pain_points"),
        "good_points": response.get("good_points"),
    }

@app.get("/settings/", response_class=HTMLResponse)
async def settings_ui():
    return get_settings_ui(supervisor_agent)

@app.post("/settings/")
async def settings_update(prompt: str = Form(...), final_output_prompt: str = Form(...)):
    """
    Endpoint to update the settings for the supervisor and final output agent.
    """
    return await update_settings(supervisor_agent, prompt, final_output_prompt)

@app.post("/test-random-user/")
async def test_random_user(first_prompt: str = Form(...)):
    """
    Test endpoint that generates a random user and processes a conversation.
    """
    random_user_id = f"user_{random.randint(1000, 9999)}"
    random_user_name = f"User{random.randint(1, 100)}"
    random_user_age = random.randint(18, 65)
    
    # Generate random values for additional user information
    current_year = 2025  # Assuming current year is 2025
    birth_year = current_year - random_user_age
    random_birthday = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{birth_year}"
    
    countries = ["Spain", "Mexico", "Argentina", "Colombia", "Chile", "USA", "France", "Germany", "Brazil", "Peru"]
    cities = {
        "Spain": ["Barcelona", "Madrid", "Valencia", "Seville"],
        "Mexico": ["Mexico City", "Guadalajara", "Monterrey"],
        "Argentina": ["Buenos Aires", "Cordoba", "Rosario"],
        "Colombia": ["Bogotá", "Medellín", "Cali"],
        "Chile": ["Santiago", "Valparaiso", "Concepción"],
        "USA": ["New York", "Los Angeles", "Chicago", "Miami"],
        "France": ["Paris", "Lyon", "Marseille"],
        "Germany": ["Berlin", "Munich", "Hamburg"],
        "Brazil": ["São Paulo", "Rio de Janeiro", "Brasilia"],
        "Peru": ["Lima", "Cusco", "Arequipa"]
    }
    
    random_country = random.choice(countries)
    random_city = random.choice(cities.get(random_country, ["Unknown"]))
    random_sex = random.choice(["Male", "Female", "Other"])
    random_has_sons = random.choice([True, False])
    random_num_sons = random.randint(1, 4) if random_has_sons else 0
    random_civil_state = random.choice(["Single", "Married", "Divorced", "Widowed", "Separated", "Partner"])

    # Simulate a conversation payload
    start_payload = {
        "type": "start",
        "user_id": random_user_id,
        "user_data": {
            "name": random_user_name,
            "age": random_user_age,
            "birthday": random_birthday,
            "country": random_country,
            "city": random_city,
            "sex": random_sex,
            "has_sons": random_has_sons,
            "num_sons": random_num_sons,
            "civil_state": random_civil_state
        }
    }
    start_response = await handle_conversation(start_payload)

    # Simulate a prompt payload using the provided first_prompt
    prompt_payload = {
        "type": "prompt",
        "user_id": random_user_id,
        "data": first_prompt
    }
    prompt_response = await handle_conversation(prompt_payload)

    # Simulate stopping the conversation
    stop_payload = {
        "type": "stop",
        "user_id": random_user_id
    }
    stop_response = await handle_conversation(stop_payload)

    return {
        "start_payload": start_payload,
        "start_response": start_response,
        "prompt_payload": prompt_payload,
        "prompt_response": prompt_response,
        "stop_payload": stop_payload,
        "stop_response": stop_response
    }