import React, { useState } from "react";
import "./App.css";

const Truebot = () => {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [selectedOption, setSelectedOption] = useState("Web");

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "user", text: input }]);  
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Truebot</h1>
      </div>

      <div className="chat-body">
        {messages.map((message, index) => (
          <div
            key={index}
            className={message.sender === "bot" ? "bot-message" : "user-message"}
          >
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Escribe tu mensaje aquí..."
          className="input-box"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <select value={selectedOption} 
          onChange={(e) => setSelectedOption(e.target.value)}
          className="select-box">  
            <option value="Reddit">Reddit</option>
            <option value="Web">Web</option>
        </select>
        <button className="send-button" onClick={handleSend}>
          Enviar
        </button>
      </div>
    </div>
  );
};

export default Truebot;