import React, { useState } from "react";
import "./App.css";

const Truebot = () => {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [selectedOption, setSelectedOption] = useState("Web");

  const sendMessage = async (url, endpoint) => {
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url, content: input }),
        });

        if (!response.ok) {
            throw new Error("Error en la solicitud al servidor");
        }

        const data = await response.json();
        
        const formatSummary = (summary) => {
          if (!summary) return ""; 
          return summary
            .split(".") 
            .map((sentence) => sentence.trim()) 
            .filter((sentence) => sentence.length > 0) 
            .join(".\n"); 
        };


        if (endpoint.includes("check_fake_news")) {
            const botMessage = `Resultado: ${data.label === 'LABEL_1' ? 'Verdadera' : 'Falsa'}\nConfianza: ${(data.score * 100).toFixed(2)}%`;
            setMessages((messages) => [
                ...messages,
                { text: botMessage, sender: "bot" },
            ]);
        } else {
          const botMessage = `Titulo: ${data.titulo}\n\nCuerpo:\n${formatSummary(data.resumen)}
          \nClasificacion:\n${data.clasificacion}`;
            setMessages((messages) => [
                ...messages,
                { text: botMessage, sender: "bot" },
            ]);
        }
    } catch (error) {
        console.error("Error:", error);
        setMessages((messages) => [
            ...messages,
            { text: "Ocurrió un error al procesar tu solicitud." + error, sender: "bot" },
        ]);
    }
};

  const handleSend = () => {
    if (input.trim()) {
      setMessages((messages) => [
        ...messages,
        { text: input, sender: "user" }, 
      ]);

      if (selectedOption === "Reddit") {
        sendMessage(input, "http://127.0.0.1:5000/reddit");
      } else if (selectedOption === "Web") {
        sendMessage(input, "http://127.0.0.1:5000/Web");
      }
      else if (selectedOption === "Texto") {
        /*Para cuando agreguemos el bert conversacional
        sendMessage(input, "Ya veremos"); */
      }
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
        <select 
          value={selectedOption} 
          onChange={(e) => setSelectedOption(e.target.value)}
          className="select-box"
        >  
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
