from typing import List, Dict, Any, Optional
from agents import Agent, OpenAIChatCompletionsModel, RunResult
from agents import Runner
from transformers.html_transformer import HTMLTransformer
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT

class MainAgentOutput(BaseAgentOutput):
    """
    Output model for the Main Assistant.
    """
    # additional_info: Optional[str] = None  # Add any specific fields for the main agent if needed

class Supervisor:
    def __init__(self, agents: List[Agent], model: OpenAIChatCompletionsModel, prompt: str, html_transformer: HTMLTransformer):
        self.agents = agents

        self.html_transformer = html_transformer

        # Create the main assistant agent
        self.main_assistant = Agent(
            name="Main Assistant",
            instructions=(
                BASE_STARTING_PROMPT +
                prompt  # Use the provided prompt
            ),
            model=model,
            handoffs=agents,
            output_type=MainAgentOutput  # Use the base output type with optional extensions
        )

    async def process_input(self, input_text: str) -> RunResult:
        """
        Routes the input to the appropriate agent and returns the result.
        Format input as expected by the Runner: [{"content": msg, "role": "user"}]
        """
        print(f"Using agent: {self.main_assistant.name}")  # Log the agent name

        print("Processing input...")
        print(f"Input text: {input_text}")
        
        # Format input as a list of input items with content and role
        formatted_input = [{"content": input_text, "role": "user"}]
        
        result = await Runner.run(self.main_assistant, input=formatted_input)

        result = self.html_transformer.transform_to_html(result.final_output)

        # return result.final_output

        return result

