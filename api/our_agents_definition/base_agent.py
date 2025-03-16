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
Se conciso con tu respuesta y proporciona información relevante. No busques información adicional a menos que sea necesario. 
Si necesitas realizar una búsqueda en internet, puedes hacerlo.
Solo da respuestas muy cortas y directas. Don't be verbose.
"""
