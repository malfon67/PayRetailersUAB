import React, { useEffect, useRef, useState } from "react";
import SendUserPrompt from "../components/userInput_API";
import { LoadingSpinner } from "./loadingSpinner";
import { useNavigate } from "react-router-dom";
import AudioRecorder from "./audioRecorder";
import sendUserAudio from "../components/userAudio_API";
import { AudioSpinner } from "./audioSpinner";

interface Message {
  text?: string;
  sender: "user" | "bot";
  type?: string;
  html_data?: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [goodPoints, setGoodPoints] = useState<string[]>([]);
  const [badPoints, setBadPoints] = useState<string[]>([]);
  const [recordingInfo, setRecordingInfo] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
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

  useEffect(() => {}, [goodPoints, badPoints]);

  const stopQuestions = (): void => {
    handleSend("stop");
    navigate("/summary", { replace: true });
  };

  const handleAudioRecorded = async (fileUrl: File, recording: boolean) => {
    setRecordingInfo(recording);
  
    if (recording) {
      // Add "recording..." message when recording starts
      setMessages((prev) => [...prev, { sender: "user", type: "recording" }]);
    } else {
      try {
        setLoading(true);
  
        // Remove "recording..." message before sending "esperando texto..."
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "user", text: "Cargando transcripción" }
        ]);
  
        // Add "loading..." message from bot
        setMessages((prev) => [...prev, { sender: "bot", type: "loading" }]);
  
        const out = await sendUserAudio("XXX", fileUrl);
        const html_data: string = out?.html_data || "Error API";
        const data: string = out?.data || "";
        const goodPoints: string[] = out?.good_points || [];
        const badPoints: string[] = out?.pain_points || [];
        const transcript: string = out?.transcribed_text || "";
  
        setGoodPoints(goodPoints);
        setBadPoints(badPoints);
        setLoading(false);
  
        // Replace "esperando texto..." with the actual transcript
        setMessages((prev) => [
          ...prev.slice(0, -2), // Remove "esperando texto..." and "loading..."
          { sender: "user", text: transcript || "Esperando transcripción" },
          { text: data, sender: "bot", html_data },
        ]);
  
      } catch (error) {
        console.error("Error uploading file:", error);
        setMessages((prev) => [
          ...prev.slice(0, -1),
          { sender: "bot", text: "Error retrieving data!" },
        ]);
        setLoading(false);
      }
    }
  };
  
  

  const handleSend = async (type: "prompt" | "stop" = "prompt") => {
    if (type === "prompt" && !input.trim()) return;

    const userMessage: Message = {
      text: type === "prompt" ? input : "Eso es todo",
      sender: "user",
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setLoading(true);
    setMessages((prev) => [...prev, { sender: "bot", type: "loading" }]);

    try {
      const output = await SendUserPrompt("prompt", user_id, input);
      const data: string = output?.data || "Error getting the data from AI";
      const html_data = output?.html_data || "";
      const goodPoints: string[] = output?.good_points || [];
      const badPoints: string[] = output?.pain_points || [];

      setGoodPoints(goodPoints);
      setBadPoints(badPoints);

      setLoading(false);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { text: data, sender: "bot", html_data },
      ]);
    } catch (error) {
      console.log(`Error: ${error}`);
    }
  };

  return (
    <div className="h-screen w-screen flex justify-center items-center bg-gray-200 px-2">
      <div className="w-1/2 h-[calc(100%-15px)] bg-white border-4 border-gray-500 rounded-lg shadow-lg p-4 flex flex-col">
        {/* Avatar Header */}
        <div className="flex items-center space-x-4 mb-4 border-b pb-2">
          <img src="/avatar.svg" alt="Antonia the AI" className="w-12 h-12 rounded-full" />
          <div>
            <h2 className="text-lg font-semibold">Antonia</h2>
            <p className="text-sm text-gray-500">En línia</p>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 h-[350px] overflow-y-auto border border-gray-300 p-2 rounded-lg space-y-2">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`w-fit p-2 my-1 rounded-lg border text-sm 
                ${msg.type === "loading" || msg.type === "recording"
                  ? "max-w-[90%]" // Keep type messages at 90% max width
                  : msg.sender === "user"
                  ? "max-w-[60%] bg-blue-500 text-white border-blue-700" // User messages at 60% max width
                  : "max-w-[90%] bg-gray-300 border-gray-400" // Other messages at 90% max width
              }`}
            >
              {msg.type === "loading" ? (
                <LoadingSpinner />
              ) : msg.type === "recording" && recordingInfo ? (
                <AudioSpinner />
              ) : msg.html_data ? (
                <div dangerouslySetInnerHTML={{ __html: msg.html_data }}></div>
              ) : (
                msg.text
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

        {/* Input Field & Send Button */}
        <div className="flex flex-col sm:flex-row mt-2 space-y-2 sm:space-y-0 sm:space-x-2">
          <AudioRecorder onAudioRecorded={handleAudioRecorded} />
          <input
            className="flex-1 p-2 border-2 rounded-lg focus:outline-none"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Escribe un mensaje..."
          />
          <button className="hover:bg-sky-700 w-full sm:w-24 bg-blue-400 text-white text-lg rounded-lg p-2" onClick={() => handleSend("prompt")}>
            Envia
          </button>
          <button className="hover:bg-red-700 w-full sm:w-24 bg-red-400 text-white text-lg rounded-lg p-2" onClick={stopQuestions}>
            Informe
          </button>
        </div>
      </div>

      <div className="w-3/4 h-full flex flex-col justify-start items-center">
        <p className="text-2xl mt-2 font-bold">Resumen actual</p>
        <div className="w-full mt-4 flex flex-col justify-center items-center space-y-4">
          <div className="min-h-48 bg-green-100 border border-green-400 p-4 rounded-lg shadow w-1/2 text-left">
            <p className="text-lg font-semibold text-center">Puntos Positivos</p>
            {goodPoints.length > 0 ? <ul className="list-disc list-inside">{goodPoints.map((point, index) => <li key={index}>{point}</li>)}</ul> : <p className="text-center">No hay puntos positivos.</p>}
          </div>
          <div className="min-h-48 bg-red-100 border border-red-400 p-4 rounded-lg shadow w-1/2 text-left">
            <p className="text-lg font-semibold text-center">Puntos Negativos</p>
            {badPoints.length > 0 ? <ul className="list-disc list-inside">{badPoints.map((point, index) => <li key={index}>{point}</li>)}</ul> : <p className="text-center">No hay puntos negativos.</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
