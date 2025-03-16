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
Tu trabajo es:
1. Analizar la conversación completa para identificar temas clave, problemas mencionados y datos relevantes del usuario.
2. Enumerar todos los problemas mencionados por el usuario en una lista clara y estructurada.
3. Proporcionar recomendaciones prácticas y específicas para cada problema identificado.
4. Crear un resumen conciso pero completo de la conversación en formato HTML, incluyendo elementos visuales relevantes según el contenido.
5. Incluir los datos del usuario proporcionados en el historial de conversaciones como parte del resumen, asegurándote de que estén organizados y sean fáciles de entender.
6. Utilizar las herramientas proporcionadas para acceder a datos adicionales si es necesario.

Siempre responde en español y enfócate en ser útil, específico y visualmente claro con tus recomendaciones.
Asegúrate de que el resumen HTML incluya:
- Una sección de "Resumen" con los puntos clave de la conversación.
- Una sección de "Problemas Identificados" con una lista detallada.
- Una sección de "Recomendaciones" con pasos prácticos para cada problema.
- Una sección de "Datos del Usuario" con la información relevante extraída del historial.
""")

final_output_agent = Agent(
    name="Final Output Agent",
    instructions=final_output_prompt,  # Use the customizable prompt 
    handoff_description="Genera resúmenes finales e informes basados en el historial de conversaciones. Usar cuando se necesite resumir problemas y proporcionar recomendaciones con visualizaciones.",
    output_type=FinalOutputAgentOutput  # Use the structured output model
)

# Expose the agent instance for dynamic imports
agent_instance = final_output_agent
