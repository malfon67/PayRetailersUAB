const prompt_url = "https://e60b-158-109-94-92.ngrok-free.app/process-input";

interface PromptResponse {
  data?: string; // Adjust type based on actual API response
  error?: string;
  html_data?: string;
  good_points?: Array<string>;
  pain_points?: Array<string>;
}

export default async function sendUserPrompt(
  promptType: string,
  userID: string,
  prompt: string
): Promise<PromptResponse> {
  try {
    const response = await fetch(prompt_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: promptType,
        user_id: userID,
        data: prompt,
      }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const result: PromptResponse = await response.json();
    console.log(`Respa: ${result}`);
    return result; // Return typed data
  } catch (error) {
    console.error("Error fetching data:", error);
    return { error: (error as Error).message }; // Ensure consistent return type
  }
}