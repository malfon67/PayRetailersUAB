from pydantic import BaseModel
from typing import Optional

class BaseAgentOutput(BaseModel):
    """
    Base class for agent outputs. All agents must include these attributes.
    """
    agent_type: str
    status: str
    data: Optional[str] = None

# Base starting prompt for all agents
BASE_STARTING_PROMPT = """
Tu salida debe estar en formato HTML y utilizar clases de Tailwind CSS para que pueda renderizarse correctamente en el frontend.
Asegúrate de que el diseño sea claro, accesible y visualmente atractivo. Genera contenido relevante y útil para el usuario, conciso no muy largo.
Sobretodo, utiliza CSS para darle estilo a tu salida y hacerla atractiva.
Utiliza tailwind por ejemplo para las negritas, itálicas, tamaños de letra, colores, etc.
UTILIZA SIEMPRE TAILWIND CSS PARA TODO. 
"""
