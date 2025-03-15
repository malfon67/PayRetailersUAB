import asyncio
import os
import uuid

from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, OpenAIChatCompletionsModel, RawResponsesStreamEvent, Runner, TResponseInputItem, set_default_openai_client, trace

# Load environment variables
load_dotenv()

llm_model_name = os.getenv("GPT4O_MINI_DEPLOYMENT")

# Create OpenAI client using Azure OpenAI
openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=llm_model_name
)

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client, False)

azure_model = OpenAIChatCompletionsModel(
    model=llm_model_name,
    openai_client=openai_client,
)

"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model=azure_model,
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
    model=azure_model,
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model=azure_model,
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
    model=azure_model,
)


async def main():
    # We'll create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    msg = input("Hi! We speak French, Spanish and English. How can I help? ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    while True:
        # Each conversation turn is a single trace. Normally, each input from the user would be an
        # API request to your app, and you can wrap the request in a trace()
        with trace("Routing example", group_id=conversation_id):
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                print(data)
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n")

        inputs = result.to_input_list()
        print("\n")

        user_msg = input("Enter a message: ")
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent


if __name__ == "__main__":
    asyncio.run(main())