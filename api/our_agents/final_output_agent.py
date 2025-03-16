from agents import Agent, function_tool
from our_agents_definition.base_agent import BaseAgentOutput
# from settings import load_settings  # Import settings to load the prompt
from settings import load_prompt, FINAL_OUTPUT_PROMPT_FILE  # Import the new load_prompt function
from typing import List, Optional

class FinalOutputAgentOutput(BaseAgentOutput):
    """
    Structured output model for the Final Output Agent.
    """
    html_summary: str
    problems: List[str]
    recommendations: List[str]
    user_data: Optional[dict] = None


# Load the customizable prompt from the plain text file
final_output_prompt = load_prompt(FINAL_OUTPUT_PROMPT_FILE, """
Eres responsable de generar un resumen final basado en el historial de conversaciones proporcionado.
Tu salida debe estar en formato HTML y utilizar clases de Tailwind CSS para que pueda renderizarse correctamente en el frontend.
Incluye:
- Una sección de "Resumen" con los puntos clave de la conversación.
- Una sección de "Problemas Identificados" con una lista detallada.
- Una sección de "Recomendaciones" con pasos prácticos para cada problema.
- Una sección de "Datos del Usuario" con la información relevante extraída del historial.
Asegúrate de que el diseño sea claro, accesible y visualmente atractivo.
""")

final_output_agent = Agent(
    name="Final Output Agent",
    instructions=final_output_prompt,  # Use the customizable prompt
    handoff_description="Genera resúmenes finales e informes basados en el historial de conversaciones. Genera tu salida en formato JSON, y esta será transformada a HTML por el HTMLTransformer.",
    output_type=FinalOutputAgentOutput  # Use the structured output model
)

# Expose the agent instance for dynamic imports
agent_instance = final_output_agent
