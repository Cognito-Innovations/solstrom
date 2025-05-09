import React, { useEffect, useRef, useState } from "react";
import { sendMessage } from "./common/api.services";
import { TypingLoader } from "./components/TypingLoader/TypingLoader";
import { Message, ProjectAgentResponse } from "./common/types";
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
      const response = await sendMessage(input.trim());

      // Handle project agent response as structured data
      if (response && response.response && Array.isArray(response.response)) {
        const botMessage: Message = {
          text: "",
          sender: "bot",
          projectData: {
            points: response.response,
            is_greeting: response?.is_greeting,
            exists_in_data: response?.exists_in_data,
            exists_elsewhere: response?.exists_elsewhere,
            relevant_projects: response?.relevant_projects || [],
          }
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        // Fallback for old format or error messages
        setMessages((prev) => [
          ...prev,
          { text: response.response || "No response received", sender: "bot" },
        ]);
      }
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

  const renderProjectResponse = (data: ProjectAgentResponse) => {
    // For greetings, show a cleaner welcome message without scores
    if (data.is_greeting) {
      return (
        <div className="greetingResponse">
          {data.points.map((point, i) => (
            <div key={i} className="welcomePoint">{point}</div>
          ))}


        </div>
      );
    }

    // For project validation responses
    return (
      <div className="projectResponse">
        {data.points.map((point, i) => (
          <div key={i} className="responsePoint">{point}</div>
        ))}

        <div className="metaInfo">


          {data.relevant_projects && data.relevant_projects?.length > 0 && (
            <div className="section">
              <h4>Related Projects:</h4>
              <ul>
                {data.relevant_projects.map((project, i) => (
                  <li key={i}>{project}</li>
                ))}
              </ul>
            </div>
          )}

  
        </div>
      </div>
    );
  };

  return (
    <div className={'chatWrapper'}>
      <div className="messagesWrapper">
        {messages.length === 0 && (
          <div className="placeholder">What Solana project can I validate for you?</div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.sender === "user" ? "userMessage" : "botMessage"}
          >
            {msg.projectData
              ? renderProjectResponse(msg.projectData)
              : msg.text}
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
          placeholder="Enter a Solana project to validate"
        />
        <button onClick={handleSend} disabled={isLoading}>↩</button>
      </div>
    </div>
  );
};

export default App;