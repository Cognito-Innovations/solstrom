import React from "react";
import "./TypingLoader.scss";

export const TypingLoader: React.FC = () => {
  return (
    <div className="typing-loader">
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );
};