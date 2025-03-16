from our_agents_definition.base_agent import BaseAgentOutput

import groq


class HTMLTransformer:
    
    def __init__(self, llm_client, llm_model_name):
        """
        Initialize the HTMLTransformer with an LLM client.

        Parameters:
        - llm_client: The LLM client to use for generating HTML
        """
        self.llm_client = llm_client
        self.llm_model_name = llm_model_name

    def transform_to_html(self, data: dict) -> str:
        """
        Use the LLM client to transform the given data into a well-structured HTML.

        Parameters:
        - data: The data to transform

        Returns:
        - HTML string generated by the LLM
        """

        class HtmlOutput(BaseAgentOutput):
            """
            Output model for the Health Agent.
            """

        print("Transforming data into HTML...")

        prompt = (
            "Transform the following input data into a well-structured HTML using Tailwind CSS. "
            "Ensure the HTML is visually appealing and includes modern, responsive UI components such as cards, tables, lists"
            "Use Tailwind CSS classes to style the components for a clean and professional design. "
            "The layout should be user-friendly, accessible, and optimized for readability. "
            "Incorporate appropriate headings, sections, and interactive elements where relevant. "
            "The response must only contain valid HTML code and nothing else. "
            "Do not include any explanations, comments, or additional text outside the HTML.\n\n"
            "It should start with <!DOCTYPE html> or <html> to be a correct HTML.\n\n"
            "Prioritize nicer over speed.\n\n Don't include \n on the code"
            "You will be on a smartphone so make sure it looks good on a small screen.\n\n"
            f"Input Data: {data.data}"
        )

        # print(prompt)
        
        # # for attempt in range(3):  # Retry up to 3 times
        # response = self.llm_client.beta.chat.completions.parse(
        #     model=self.llm_model_name,
        #     messages=[{"role": "system", "content": prompt}],
        #     response_format=HtmlOutput
        # ).choices[0].message.parsed

        chat_completion = self.llm_client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": prompt
            }
            ],
            model="llama-3.3-70b-versatile",
        )
        # print(chat_completion.choices[0].message.content)
        response = chat_completion.choices[0].message.content
            

        if response is None:
            return "Error data is None"

        if response.strip().startswith("<!DOCTYPE html>") or response.strip().startswith("<html"):
            # print(f"Generated HTML: {response}")
            return HtmlOutput(agent_type="html", status="success", data=response)
        
        else:
            return HtmlOutput(agent_type="html", status="success", data=response)

            # print(f"Attempt {attempt + 1}: Invalid HTML response, retrying...")

        # raise ValueError("Failed to generate valid HTML after 3 attempts.")