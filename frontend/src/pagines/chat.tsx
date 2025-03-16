import React, { useEffect, useRef, useState } from "react";
import SendUserPrompt from "../components/endpoints_marc";
import { LoadingSpinner } from "./loadingSpinner";

// Define message type
interface Message {
  text: string;
  sender: "user" | "bot";
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null); // Ref for auto-scrolling

  const user_id = "prova";
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

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // Clear input
    setLoading(true);

    // Add a loading message from the bot
    setMessages((prev) => [...prev, { sender: "bot", text: "loading..." }]);

    const type = "prompt";
    try {
      const output = await SendUserPrompt(type, user_id, input);
      const data = output?.data || "Error retrieving the data!";

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
        {/* Messages Area */}
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
          {/* Invisible div to track the bottom */}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Field & Send Button */}
        <div className="flex mt-2">
          <input
            className="flex-1 p-2 border-2 rounded-lg focus:outline-none"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
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
            onClick={handleSend}
          >
            Finaliza
          </button>
        </div>
      </div>
    </div>
  );
}
