from typing import List, Dict, Any
from agents import Agent, OpenAIChatCompletionsModel, RunResult
from agents import Runner

class Supervisor:
    def __init__(self, agents: List[Agent], model: OpenAIChatCompletionsModel, prompt: str):
        self.agents = agents

        # Create the main assistant agent
        self.main_assistant = Agent(
            name="Main Assistant",
            instructions=prompt,  # Use the provided prompt
            model=model,
            handoffs=agents,
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
        return result



