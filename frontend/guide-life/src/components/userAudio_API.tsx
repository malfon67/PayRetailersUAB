const prompt_url = "https://f7ae-158-109-94-92.ngrok-free.app/audio-input";

interface PromptResponse {
  user_id?: string;
  data?: string;
  html_data?: string;
  good_points?: Array<string>;
  pain_points?: Array<string>;
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
    return result;
  } catch (error) {
    console.error("Error fetching data:", error);
    return {};
  }
}