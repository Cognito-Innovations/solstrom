import React, { useEffect, useRef, useState } from "react";
import "./App.scss";

interface Message {
  text: string;
  sender: "user" | "bot";
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };


  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMessage: Message = { text: input.trim(), sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { text: "Hey there! How can I help you today?", sender: "bot" },
      ]);
    }, 500);
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
        <button onClick={handleSend}>↩</button>
      </div>
    </div>
  );
};

export default App;
