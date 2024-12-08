import React, { useState } from "react";
import "./App.css";

const Truebot = () => {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [selectedOption, setSelectedOption] = useState("Web");

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

        if (endpoint.includes("check_fake_news")) {
            const botMessage = `Resultado: ${data.label === 'LABEL_1' ? 'Verdadera' : 'Falsa'}\nConfianza: ${(data.score * 100).toFixed(2)}%`;
            setMessages((messages) => [
                ...messages,
                { text: botMessage, sender: "bot" },
            ]);
        } else {
            const botMessage = `Titulo: ${data.titulo}\n\nCuerpo:\n${wrapText(data.content, 100)}`;
            setMessages((messages) => [
                ...messages,
                { text: botMessage, sender: "bot" },
            ]);
        }
    } catch (error) {
        console.error("Error:", error);
        setMessages((messages) => [
            ...messages,
            { text: "Ocurrió un error al procesar tu solicitud.", sender: "bot" },
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
      }else if (selectedOption === "FakeNews") {
        sendMessage(input, "http://127.0.0.1:5000/check_fake_news"); // Nueva ruta
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
          <option value="FakeNews">Detectar Fake News</option>

        </select>
        <button className="send-button" onClick={handleSend}>
          Enviar
        </button>
      </div>
    </div>
  );
};

export default Truebot;
