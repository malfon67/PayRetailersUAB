const prompt_url = "https://f7ae-158-109-94-92.ngrok-free.app/audio-input";

interface PromptResponse {
  user_id?: string; // Adjust type based on actual API response
  data?: string;
  goodPoints?: Array<string>;
  badPoints?: Array<string>;
}

export default async function sendUserAudio(
  userID: string,
  file: File
): Promise<PromptResponse> {
  try {
    const formData = new FormData();
    formData.append("user_id", userID);
    formData.append("file", file);

    const response = await fetch(prompt_url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const result: PromptResponse = await response.json();
    console.log("Audio Response:", result);
    return result;
  } catch (error) {
    console.error("Error fetching data:", error);
    return {};
  }
}