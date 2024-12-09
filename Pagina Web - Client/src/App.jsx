import React, { useState } from "react";
import "./App.css";

const Truebot = () => {
  const [messages, setMessages] = useState([]); 
  const [input, setInput] = useState(""); 
  const [selectedOption, setSelectedOption] = useState("Web");
  const [isThinking, setIsThinking] = useState(false);

  const isValidUrl = (url) => {
    const urlPattern = new RegExp(
      "^(https?:\\/\\/)" + 
      "((([a-zA-Z0-9$._%+-]+)@)?[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6})" + 
      "(\\:\\d+)?(\\/[-a-zA-Z0-9%._~+&]*)*" + 
      "(\\?[;&a-zA-Z0-9%._~+=-]*)?" + 
      "(\\#[-a-zA-Z0-9%._]*)?$", 
      "i"
    );
    return urlPattern.test(url);
  };

  const formatSummary = (summary) => {
    if (!summary) return [];
    
    if (Array.isArray(summary)) {
      return summary
        .map((sentence, index) => (
          <div key={index} style={{ marginBottom: "10px" }}>
            {sentence.trim()}
          </div>
        ));
    }

    return summary
      .split(".")
      .map((sentence, index) => (
        <div key={index} style={{ marginBottom: "10px" }}>
          {sentence.trim()}
        </div>
      ))
      .filter((sentence) => sentence.props.children.length > 0); 
  };

  const sendMessage = async (url, endpoint) => {
    setIsThinking(true); 
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
  
      const formattedSummary = formatSummary(data.resumen); 
      const botMessage = (
        <div>
          <div><strong>Titulo:</strong> {data.titulo}</div>
          <div><strong>Cuerpo:</strong></div>
          {formattedSummary}
          <div><strong>Clasificacion:</strong> {data.clasificacion}</div>
        </div>
      );
  
      setMessages((messages) => [
        ...messages,
        { text: botMessage, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((messages) => [
        ...messages,
        { text: "Ocurrió un error al procesar tu solicitud. " + error, sender: "bot" },
      ]);
    } finally {
      setIsThinking(false); 
    }
  };

  const handleSend = () => {
    if (!input.trim()) return;
  
    if (!isValidUrl(input)) {
      setMessages((messages) => [
        ...messages,
        { text: input, sender: "user" },
        { text: "Por favor, ingrese un enlace válido para generar una predicción.", sender: "bot" },
      ]);
      setInput("");
      return;
    }
  
    if (selectedOption === "Web" && input.includes("reddit")) {
      setMessages((messages) => [
        ...messages,
        { text: input, sender: "user" },
        { text: "No se aceptan enlaces de Reddit en la opción Web.", sender: "bot" },
      ]);
      setInput("");
      return;
    }

    if (selectedOption === "Reddit" && !input.includes("reddit.com")) {
      setMessages((messages) => [
        ...messages,
        { text: input, sender: "user" },
        { text: "Solo se aceptan enlaces de Reddit en la opción Reddit.", sender: "bot" },
      ]);
      setInput("");
      return;
    }
  
    setMessages((messages) => [
      ...messages,
      { text: input, sender: "user" }, 
    ]);
  
    if (selectedOption === "Reddit") {
      sendMessage(input, "http://127.0.0.1:5000/reddit");
    } else if (selectedOption === "Web") {
      sendMessage(input, "http://127.0.0.1:5000/Web");
    }
    setInput(""); 
  };

  const handleOptionChange = (e) => {
    const newOption = e.target.value;
    setSelectedOption(newOption);
    setMessages([]);
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
            className={message.sender === "bot" ? "bot-message" : "user-message"}>
            {message.sender === "bot" ? (
              typeof message.text === "string" ? (
                <pre>{message.text}</pre>
              ) : (
                message.text 
              )
            ) : (
              <p>{message.text}</p>
            )}
          </div>
        ))}
        {isThinking && (
          <div className="bot-message">
            <p className="thinking-animation">...</p>
          </div>
        )}
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
          onChange={handleOptionChange}
          className="select-box"
        >  
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
