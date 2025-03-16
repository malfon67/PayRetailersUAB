from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from typing import Union, Optional  # Import Optional for type hinting
import io
from agent_manager import supervisor_agent, handle_conversation  # Import supervisor_agent and handle_conversation
from settings import get_settings_ui, update_settings, load_whisper_model_name  # Import settings functions
import random

from dotenv import load_dotenv
import os

load_dotenv()
from groq import Groq


USE_LOCAL_WHISPER_API = os.environ.get("USE_LOCAL_WHISPER_API", "false").lower() == "true"


if USE_LOCAL_WHISPER_API:
    import whisper  
    

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
from html_templates import generate_html_from_json  # Import the HTML templates module
import tempfile # Import the tempfile module for temporary file handling

# Set up Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"))

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

if USE_LOCAL_WHISPER_API:
    # Load the Whisper model dynamically
    def load_whisper_model():
        model_name = load_whisper_model_name()
        return whisper.load_model(model_name)

    whisper_model = load_whisper_model()

# Function to transcribe audio using Groq's Whisper API
def transcribe_audio_with_groq(audio_file_path: str) -> str:
    """
    Transcribe audio using Groq's Whisper implementation.
    """
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3",
                prompt="""Transcribe the audio to text. Always respond in Spanish.""",
                response_format="text",
                language="es",
            )
        return transcription  # This is now directly the transcription text
    except Exception as e:
        print(f"An error occurred with Groq transcription: {str(e)}")
        return "Transcription failed with Groq."

# Updated function to transcribe audio using the selected method
def transcribe_audio(audio_file: io.BytesIO) -> str:
    """
    Transcribes audio using either the local Whisper model or Groq's Whisper API based on configuration.
    """
    if USE_LOCAL_WHISPER_API:
        print("Using local Whisper model for transcription.")
        audio_file.seek(0)  # Ensure the file pointer is at the beginning
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name
        result = whisper_model.transcribe(temp_audio_path)
        os.unlink(temp_audio_path)  # Clean up temporary file
        print(result)
        return result.get("text", "Transcription failed")
    else:
        print("Using Groq's Whisper API for transcription.")
        # Save the input audio file temporarily
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name
        transcription = transcribe_audio_with_groq(temp_audio_path)
        os.unlink(temp_audio_path)  # Clean up temporary file
        return transcription
        

async def process(payload: dict, transcribed_text: str = None):
    """
    Process the conversation based on the provided payload.
    """
    # Handle the conversation using the supervisor agent
    response = await handle_conversation(payload)

    # Handle errors returned by the conversation handler
    if "error" in response:
        return JSONResponse(content={"error": response["error"]}, status_code=response.get("status_code", 400))

    # # Check if the response is from the main agent and set agent_type to "main"
    # if "last_agent" not in response:
    #     response["last_agent"] = "main"

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
        "transcribed_text": transcribed_text if transcribed_text else None
    }
 
@app.post("/process-input/")
async def process_input(payload: dict = Body(...)):
    """
    Handles the conversation flow based on the provided JSON schema.
    """
    return await process(payload)
    

@app.post("/audio-input/")
async def audio_input(file: UploadFile = File(...), user_id: str = Form(...)):
    """
    Endpoint to handle audio input, transcribe it to text, and process it with the AI.
    """
    # Read the uploaded audio file
    audio_bytes = io.BytesIO(await file.read())
    
    # Transcribe the audio to text
    transcribed_text = transcribe_audio(audio_bytes)
    
    # Create a payload for the conversation handler
    payload = {
        "type": "prompt",
        "user_id": user_id,
        "data": transcribed_text
    }

    return await process(payload, transcribed_text)

@app.get("/settings/", response_class=HTMLResponse)
async def settings_ui():
    return get_settings_ui(supervisor_agent)

@app.post("/settings/")
async def settings_update(
    prompt: str = Form(...), 
    final_output_prompt: str = Form(...), 
    whisper_model_param: Optional[str] = Form(None)  # Make whisper_model_param optional
):
    """
    Endpoint to update the settings for the supervisor, final output agent, and Whisper model.
    """
    global whisper_model  # Declare whisper_model as global
    if whisper_model_param:  # Only update the Whisper model if a value is provided
        response = await update_settings(supervisor_agent, prompt, final_output_prompt, whisper_model_param)
        whisper_model = load_whisper_model()  # Reload the Whisper model with the new settings
    else:
        response = await update_settings(supervisor_agent, prompt, final_output_prompt, "")
    return response

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