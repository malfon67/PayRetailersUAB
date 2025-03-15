import asyncio
import requests
import re
import json
from agents import Agent, function_tool
from html_templates import generate_html_from_json  # Import the HTML templates module
# from settings import load_settings  # Import settings to load the prompt
from settings import load_prompt, FINAL_OUTPUT_PROMPT_FILE  # Import the new load_prompt function

@function_tool
def generate_html_output(conversation: str, user_data: str = None) -> str:
    """
    Generate an HTML formatted output based on the conversation analysis.
    
    Parameters:
    - conversation: The full conversation text to analyze
    - user_data: JSON string with user information (optional)
    
    Returns:
    - HTML formatted output using the html_templates module
    """
    print("Final Output Agent is generating HTML output.")
    
    # Extract information from conversation
    problems = extract_problems(conversation)
    recommendations = generate_recommendations(problems, conversation)
    
    # Prepare the JSON response to pass to the HTML generator
    response = {
        "type": "final_summary",
        "status": "success",
        "problems": problems,
        "recommendations": recommendations,
        "user_data": json.loads(user_data) if user_data else None
    }
    
    # Use the HTML templates module to generate the output
    html_output = generate_html_from_json(response)
    return html_output

def extract_problems(conversation: str) -> list:
    """Extract problems from the conversation text"""
    # This is a simplified version - in a real implementation, 
    # you might use more sophisticated NLP techniques
    problems = []
    
    # Look for mention of problems in the conversation
    problem_indicators = [
        r"(?:tengo|tiene|hay) (?:un|una|el|la) problema con ([\w\s]+)",
        r"(?:me|le) preocupa ([\w\s]+)",
        r"(?:tengo|tiene) dificultad(?:es)? (?:con|para) ([\w\s]+)",
        r"no (?:puedo|puede) ([\w\s]+)",
        r"(?:necesito|necesita) ayuda con ([\w\s]+)"
    ]
    
    for indicator in problem_indicators:
        matches = re.finditer(indicator, conversation, re.IGNORECASE)
        for match in matches:
            if match and match.group(1):
                problems.append(match.group(1).strip())
    
    # If no structured problems found, use generic ones based on keywords
    if not problems:
        if "salud" in conversation.lower() or "enfermedad" in conversation.lower():
            problems.append("Preocupaciones relacionadas con la salud")
        if "dinero" in conversation.lower() or "economía" in conversation.lower():
            problems.append("Asuntos financieros o económicos")
        if "trabajo" in conversation.lower() or "empleo" in conversation.lower():
            problems.append("Situación laboral o profesional")
            
    # If still no problems identified, add a generic one
    if not problems:
        problems.append("Consulta general de información y asesoramiento")
    
    return problems

def generate_recommendations(problems: list, conversation: str) -> list:
    """Generate recommendations based on identified problems"""
    recommendations = []
    
    for problem in problems:
        if any(health_term in problem.lower() for health_term in ["salud", "médico", "doctor", "enfermedad", "dolor"]):
            recommendations.append("Consultar con un profesional médico para una evaluación personalizada")
        
        if any(finance_term in problem.lower() for finance_term in ["dinero", "finanzas", "economía", "préstamo"]):
            recommendations.append("Revisar su situación financiera con un asesor especializado")
        
        if any(work_term in problem.lower() for work_term in ["trabajo", "empleo", "profesional", "laboral"]):
            recommendations.append("Explorar oportunidades de desarrollo profesional o formación especializada")
            
    # If no specific recommendations generated, add generic ones
    if not recommendations:
        recommendations.append("Buscar información adicional de fuentes oficiales sobre los temas consultados")
        recommendations.append("Considerar una consulta de seguimiento para profundizar en sus necesidades específicas")
    
    return recommendations



# Load the customizable prompt from the plain text file
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

final_output_agent = Agent(
    name="Final Output Agent",
    instructions=final_output_prompt,  # Use the customizable prompt
    tools=[generate_html_output],
    handoff_description="Genera resúmenes finales e informes basados en el historial de conversaciones. Usar cuando se necesite resumir problemas y proporcionar recomendaciones con visualizaciones."
)

# Expose the agent instance for dynamic imports
agent_instance = final_output_agent
