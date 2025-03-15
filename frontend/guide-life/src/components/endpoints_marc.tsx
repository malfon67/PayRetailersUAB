const prompt_url = "https://0578-158-109-94-92.ngrok-free.app/process-input";

export default async function sendUserPrompt(promptType:string, userID:string, prompt:string) {
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

    const result = await response.json();
    console.log("api response: " + result);
    return result; // Return the data for further use
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // Allow handling the error where the function is called
  }
}
