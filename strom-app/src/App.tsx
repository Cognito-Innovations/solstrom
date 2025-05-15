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
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSend = async () => {
  if (!input.trim() || isLoading) return;

  const newMessage: Message = { text: input.trim(), sender: "user" };
  setMessages((prev) => [...prev, newMessage]);
  setInput("");
  setIsLoading(true);

  try {
    const apiResponse = await sendMessage(input.trim());

    if (apiResponse?.conversation) {
      const { response, relevant_projects, sources } = apiResponse.conversation;
      
      const botMessage: Message = {
        text: "",
        sender: "bot",
        projectData: {
          points: Array.isArray(response) ? response : ["• No valid response format received"],
          is_greeting: false,
          exists_in_data: false,
          exists_elsewhere: false,
          relevant_projects: relevant_projects || [],
          sources: sources || [],
        }
      };
      setMessages((prev) => [...prev, botMessage]);
    } else {
      setMessages((prev) => [
        ...prev,
        { text: "No response received", sender: "bot" },
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


  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderProjectResponse = (data: ProjectAgentResponse) => {
  if (data.is_greeting) {
    return (
      <div className="greetingResponse">
        {data.points.map((point, i) => (
          <div key={i} className="welcomePoint">{point}</div>
        ))}
      </div>
    );
  }

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

        {data.sources && data.sources.length > 0 && (
          <div className="section">
            <h4>Sources:</h4>
            <ul className="sourcesList">
              {data.sources.map((source, i) => {
                const sourceName = typeof source === 'object' ? source.source_name : source;
                const sourceUrl = typeof source === 'object' ? source.source_url : '';
                
                return (
                  <li key={i}>
                    {sourceUrl ? (
                      <a href={sourceUrl} target="_blank" rel="noopener noreferrer">
                        {sourceName}
                      </a>
                    ) : (
                      sourceName
                    )}
                  </li>
                );
              })}
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
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter a Solana project to validate"
          rows={1}
          className="textarea-input"        
        />
        <button onClick={handleSend} disabled={isLoading}>↩</button>
      </div>
    </div>
  );
};

export default App;