import os
from fastapi import Form
from fastapi.responses import HTMLResponse, JSONResponse

SETTINGS_DIR = "/home/brunomoya/development/hackuab2025/PayRetailersUAB/settings"

# Ensure the settings directory exists
os.makedirs(SETTINGS_DIR, exist_ok=True)

SUPERVISOR_PROMPT_FILE = os.path.join(SETTINGS_DIR, "supervisor_prompt.txt")
FINAL_OUTPUT_PROMPT_FILE = os.path.join(SETTINGS_DIR, "final_output_prompt.txt")

# Load a prompt from a file
def load_prompt(file_path: str, default: str) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return default

# Save a prompt to a file
def save_prompt(file_path: str, prompt: str):
    with open(file_path, "w") as file:
        file.write(prompt)

def get_settings_ui(supervisor_agent) -> HTMLResponse:
    # Render a simple HTML form for modifying the supervisor's and final output agent's settings
    supervisor_prompt = load_prompt(SUPERVISOR_PROMPT_FILE, "This agent provides assistance with general queries.")
    final_output_prompt = load_prompt(FINAL_OUTPUT_PROMPT_FILE, """
Eres responsable de generar un resumen final basado en el historial de conversaciones proporcionado.
Tu trabajo es:
1. Analizar la conversación completa para identificar temas clave y problemas mencionados
2. Enumerar todos los problemas mencionados por el usuario
3. Proporcionar recomendaciones prácticas para cada problema
4. Crear un resumen conciso pero completo de la conversación
5. Utilizar las herramientas proporcionadas para acceder a datos adicionales si es necesario
6. Generar un output en HTML con elementos visuales relevantes según el contenido

Siempre responde en español y enfócate en ser útil y específico con tus recomendaciones.
Asegúrate de incluir visualizaciones adecuadas (como mapas para ubicaciones o gráficos para datos financieros).
""")
    return HTMLResponse(f"""
    <html>
        <head>
            <title>Agent Settings</title>
        </head>
        <body>
            <h1>Modify Agent Settings</h1>
            <form action="/settings/" method="post">
                <label for="prompt">Supervisor Prompt:</label><br>
                <textarea id="prompt" name="prompt" rows="4" cols="50">{supervisor_prompt}</textarea><br><br>
                <label for="final_output_prompt">Final Output Agent Prompt:</label><br>
                <textarea id="final_output_prompt" name="final_output_prompt" rows="4" cols="50">{final_output_prompt}</textarea><br><br>
                <button type="submit">Save Settings</button>
            </form>
        </body>
    </html>
    """)

async def update_settings(supervisor_agent, prompt: Form(...), final_output_prompt: Form(...)) -> JSONResponse:
    # Extract string values from Form objects
    prompt_value = prompt if isinstance(prompt, str) else str(prompt)
    final_output_prompt_value = final_output_prompt if isinstance(final_output_prompt, str) else str(final_output_prompt)
    
    # Update the supervisor's and final output agent's prompts and save them to files
    supervisor_agent.main_assistant.instructions = prompt_value
    save_prompt(SUPERVISOR_PROMPT_FILE, prompt_value)
    save_prompt(FINAL_OUTPUT_PROMPT_FILE, final_output_prompt_value)
    return JSONResponse(content={"message": "Settings updated successfully"})
