import React, { useState } from "react";
import "./App.css";

const Truebot = () => {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [selectedOption, setSelectedOption] = useState("Web");

  const handleSend = () => {
    if (input.trim()) {
       
      setMessages((messages) => [
        ...messages,
        { text: input, sender: "user" }, 
      ]);

      const sendMessage = async () => {
        try {
          const response = await fetch("http://127.0.0.1:5000/reddit", {
            method: "POST", 
            headers: {
              "Content-Type": "application/json", 
            },
            body: JSON.stringify({
              url: input, 
            }),
          });
  
          if (!response.ok) {
            throw new Error("Error en la solicitud al servidor");
          }
  
          const data = await response.json();


          const wrapText = (text, maxLength) => {
            return text
              .split('\n')
              .map(line =>
                line.length > maxLength
                  ? line.match(new RegExp(`.{1,${maxLength}}`, 'g')).join('\n')
                  : line
              )
              .join('\n');
          };
          
          const botMessage = `Titulo: ${data.titulo}\n\nCuerpo:\n${wrapText(data.content, 100)}`;
          setMessages((messages) => [
            ...messages,
            { text: botMessage, sender: "bot" }, 
          ]);
        } catch (error) {
          console.error("Error:", error);
  
          setMessages((messages) => [
            ...messages,
            { text: "Ocurrió un error al procesar tu solicitud.", sender: "bot" },
          ]);
        }
      };
  
      sendMessage(); 
      setInput("");
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
            {message.sender === "bot" ? (
              <pre>{message.text}</pre>
            ) : (
              <p>{message.text}</p>
            )}
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
            <option value="Texto">Conversacion</option>
        </select>
        <button className="send-button" onClick={handleSend}>
          Enviar
        </button>
      </div>
    </div>
  );
};

export default Truebot;