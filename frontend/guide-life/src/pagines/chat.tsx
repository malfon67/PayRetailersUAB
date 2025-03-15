import React, { useEffect, useRef, useState } from "react";
import SendUserPrompt from "../components/userInput_API";
import { LoadingSpinner } from "./loadingSpinner";
import { useNavigate } from "react-router-dom";
import AudioRecorder from "./audioRecorder";
import sendUserAudio from "../components/userAudio_API";

interface Message {
  text: string;
  sender: "user" | "bot";
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [goodPoints, setGoodPoints] = useState<string[]>([]);
  const [badPoints, setBadPoints] = useState<string[]>([]);


  const messagesEndRef = useRef<HTMLDivElement | null>(null); // Ref for auto-scrolling
  const navigate = useNavigate();
  const user_id = "xxx";
  const defaultMsg = "Dime algo que necesite saber sobre ti...";

  useEffect(() => {
    setMessages((prev) => {
      if (prev.length === 0) {
        return [...prev, { text: defaultMsg, sender: "bot" }];
      }
      return prev;
    });
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
  }, [goodPoints, badPoints])

  const stopQuestions = (): void => {
    navigate("/summary", { replace: true });
  };

  const handleAudioRecorded = async (fileUrl: File) => {
    console.log("Received audio URL in parent:", fileUrl);
  
    try {
      await sendUserAudio("XXX", fileUrl);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleSend = async (): Promise<void> => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // Clear input
    setLoading(true);

    // Add a loading message from the bot
    setMessages((prev) => [...prev, { sender: "bot", text: "loading..." }]);

    try {
      const output = await SendUserPrompt("prompt", user_id, input);
      const data: string = output?.data || "Error getting the data from AI";
      const goodPoints: string[] = output?.goodPoints || [];
      const badPoints: string[] = output?.badPoints || [];

      setGoodPoints(goodPoints);
      setBadPoints(badPoints);

      setMessages((prev) => [
        ...prev.slice(0, -1), // Remove last "loading..." message
        { text: data, sender: "bot" },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { text: "Error retrieving the data!", sender: "bot" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen w-screen flex justify-end items-center bg-gray-200 pr-4">
      <div className="w-1/2 h-[calc(100%-15px)] bg-white border-4 border-gray-500 rounded-lg shadow-lg p-4 flex flex-col">
        <div className="flex-1 h-[350px] overflow-y-auto border border-gray-300 p-2 rounded-lg space-y-2">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`w-fit max-w-[70%] p-2 my-1 rounded-lg border text-sm ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white border-blue-700"
                    : "bg-gray-300 border-gray-400"
                }`}
              >
                {msg.text === "loading..." ? <LoadingSpinner /> : msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="flex mt-2">
        <AudioRecorder onAudioRecorded={handleAudioRecorded}/>          <input
            className="flex-1 p-2 border-2 rounded-lg focus:outline-none"
            type="text"
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === "Enter" && handleSend()}
            placeholder="Escribe un mensaje..."
          />
          <button
            className="hover:bg-sky-700 w-24 bg-blue-400 text-white text-lg rounded-lg ml-2 p-2"
            onClick={handleSend}
          >
            Envia
          </button>
          <button
            className="hover:bg-red-700 w-24 bg-red-400 text-white text-lg rounded-lg ml-2 p-2"
            onClick={stopQuestions}
          >
            Finaliza
          </button>
        </div>
      </div>

      <div className="w-1/2 flex flex-col justify-center items-center">
        <p className="text-2xl mt-2 font-bold">Resum Personal</p>

        <div className="w-full mt-4 flex justify-center items-center space-x-4">
          <div className="bg-green-100 border border-green-400 p-4 rounded-lg shadow w-1/3 text-center">
            <p className="text-lg font-semibold">Punts Positius</p>
            {goodPoints && goodPoints.length > 0 ? (
              goodPoints.map((point, index) => <p key={index}>{point}</p>)
            ) : (
              <p>No hi ha punts positius.</p>
            )}
          </div>

          <div className="bg-red-100 border border-red-400 p-4 rounded-lg shadow w-1/3 text-center">
            <p className="text-lg font-semibold">Punts Negatius</p>
            {badPoints && badPoints.length > 0 ? (
              badPoints.map((point, index) => <p key={index}>{point}</p>)
            ) : (
              <p>No hi ha punts negatius.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
