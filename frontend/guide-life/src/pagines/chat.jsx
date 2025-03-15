import React, { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    const userMessage = { text: input, sender: "user" };
    const botMessage = { text: "Hello! How can I assist you?", sender: "bot" };
    setMessages([...messages, userMessage, botMessage]);
    setInput("");
  };

  const enterPressed = () => {
    console.log("ntro");  
    handleSend()
  }

  return (
    <div className="h-screen w-screen flex justify-end items-center bg-gray-200 pr-4">
      <div className="w-96 h-3/4 bg-white border-4 border-gray-500 rounded-lg shadow-lg p-4 flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 h-[350px] overflow-y-auto border border-gray-300 p-2 rounded-lg">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`p-2 my-1 rounded-lg border ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white border-blue-700"
                    : "bg-gray-300 border-gray-400"
                }`}
              >
                {msg.text}
              </div>
            ))
          ) : (
            <p className="text-gray-400">No messages yet...</p>
          )}
        </div>

        {/* Input Field & Send Button */}
        <div className="flex mt-2">
          <input
            className="flex-1 p-2 border-2 rounded-lg focus:outline-none"
            type="text"
            value={input}
            onChange={(e) => {
              setInput(e.target.value); 
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                enterPressed(input);
              }
            }}
            placeholder="Type a message..."
          />
          <button
            className="hover:bg-sky-700 w-24 bg-blue-400 text-red-950 text-lg rounded-lg ml-2 p-2"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
