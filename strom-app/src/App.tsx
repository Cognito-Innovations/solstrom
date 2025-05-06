import React, { useEffect, useRef, useState } from "react";
import { sendMessage } from "./common/api.services";
import { TypingLoader } from "./components/TypingLoader/TypingLoader";
import { Message } from "./common/types";
import "./App.scss";

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const newMessage: Message = { text: input.trim(), sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const botResponse = await sendMessage(input.trim());
      setMessages((prev) => [
        ...prev,
        { text: botResponse, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { text: "Sorry, something went wrong. Please try again.", sender: "bot" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className={'chatWrapper'}>
      <div className="messagesWrapper">
        {messages.length === 0 && (
          <div className="placeholder">What can I help with?</div>
        )}
        
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.sender === "user" ? "userMessage" : "botMessage"}
          >
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="botMessage">
            <TypingLoader />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="inputBox">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything"
        />
        <button onClick={handleSend} disabled={isLoading}>↩</button>
      </div>
    </div>
  );
};

export default App;
