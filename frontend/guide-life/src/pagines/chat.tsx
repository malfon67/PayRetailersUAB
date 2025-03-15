import { useEffect, useState } from "react";
import SendUserPrompt from "../components/endpoints_marc";
import { LoadingSpinner } from "./loadingSpinner";

interface Message {
  text: string;
  sender: "user" | "bot";
}


export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const user_id = "prova";

  useEffect(() => {

  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return;
    // Delete the input
    setInput("");

    // Print the user message
    const userMessage: Message = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    const type = "prompt";

    setLoading(true);
    const output = await SendUserPrompt(type, user_id, input);
    setLoading(false);
    

    const data = output.data || null;
    let botMessage: Message;

    if (data != null) {
      botMessage = { text: data, sender: "bot" };
    } else {
      botMessage = { text: "Error retrieving the data!", sender: "bot" };
    }

    setMessages(prev => [...prev, botMessage]);
  };

  const enterPressed = () => {
    handleSend();
  };

  return (
    <div className="h-screen w-screen flex justify-end items-center bg-gray-200 pr-4">
      <div className="w-1/2 h-3/4 bg-white border-4 border-gray-500 rounded-lg shadow-lg p-4 flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 h-[350px] overflow-y-auto border border-gray-300 p-2 rounded-lg space-y-2">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`w-fit max-w-[70%] p-2 my-1 rounded-lg border text-sm ${
                    msg.sender === "user"
                      ? "bg-blue-500 text-black border-blue-700"
                      : "bg-gray-300 border-gray-400"
                  }`}
                > 
                {
                  loading ? (
                    <div className="flex justify-start">
                      <LoadingSpinner />
                    </div>
                  ) : (
                    msg.text
                  )
                }
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-400 text-center"></p>
          )}
        </div>

        {/* Input Field & Send Button */}
        <div className="flex mt-2">
          <input
            className="flex-1 p-2 border-2 rounded-lg focus:outline-none"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                enterPressed();
              }
            }}
            placeholder="Type a message..."
          />
          <button
            className="hover:bg-sky-700 w-24 bg-blue-400 text-white text-lg rounded-lg ml-2 p-2"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

