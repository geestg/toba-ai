import "./App.css";
import { useState, useRef } from "react";
import { destinations } from "./data/destinations";
import MapView from "./components/MapView";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [selected, setSelected] = useState(null);

  const scrollRef = useRef(null);

  // 🔥 DETECT ADA CHAT ATAU BELUM
  const hasChat = messages.length > 0;

  const scrollToDestination = (name) => {
    const index = destinations.findIndex((d) => d.name === name);
    if (index === -1 || !scrollRef.current) return;

    scrollRef.current.scrollTo({
      left: index * 260,
      behavior: "smooth",
    });
  };

  const sendMessage = async (customText) => {
    const text = customText || input;
    if (!text) return;

    setMessages((prev) => [...prev, { role: "user", text }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          lat: 2.684,
          lng: 98.875,
        }),
      });

      const data = await res.json();

      if (data.data?.chosen) {
        setSelected(data.data.chosen);
        scrollToDestination(data.data.chosen.name);
      }

      if (data.reply) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: data.reply },
        ]);
      }

      if (data.data?.route) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", route: data.data.route },
        ]);
      }

      if (data.data?.impact) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", impact: data.data.impact },
        ]);
      }

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Server error, backend lagi lucak." },
      ]);
    }

    setInput("");
  };

  return (
    <div className="app">

      {/* HERO */}
      <div className="hero">
        <img src="/images/toba.jpg" alt="Danau Toba" />
        <div className="hero-overlay">
          <h1>Toba AI</h1>
          <p>Smart Travel Assistant berbasis AI</p>

          <div className="hero-cta">
            <button
              className="primary"
              onClick={() =>
                sendMessage("Rekomendasikan tempat terbaik hari ini")
              }
            >
              Explore AI
            </button>

            <button
              className="secondary"
              onClick={() =>
                document
                  .querySelector(".destination-wrapper")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              Lihat Destinasi
            </button>
          </div>
        </div>
      </div>

      {/* SECTION */}
      <div className="section">
        <h2>Destinasi Populer</h2>
        <p>Mau kemana nih lek?</p>
      </div>

      {/* 🔥 DESTINATION (AUTO SHRINK) */}
      <div className={`destination-wrapper ${hasChat ? "shrink" : ""}`}>
        <div className="card-container single" ref={scrollRef}>
          {destinations.map((d, i) => (
            <div
              key={i}
              className={`card ${i === 0 ? "featured" : ""} ${
                selected?.name === d.name ? "active" : ""
              }`}
              onClick={() => sendMessage(`Saya mau ke ${d.name}`)}
            >
              <img src={d.img} alt={d.name} />
              <div className="card-overlay">
                <h3>{d.name}</h3>
                <span>⭐ {d.rating}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 🔥 CHAT (MAIN FOCUS) */}
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-row ${msg.role}`}>

            {msg.text && (
              <div className="chat-bubble">
                {msg.text}
              </div>
            )}

            {msg.route && (
              <div className="chat-map">
                <MapView route={msg.route} />
              </div>
            )}

            {msg.impact && (
              <div className="chat-impact">
                Crowd: {msg.impact.before} → {msg.impact.after}
              </div>
            )}

          </div>
        ))}
      </div>

      {/* INPUT */}
      <div className="chat-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Mau kemana hari ini lek..."
        />
        <button onClick={() => sendMessage()}>➤</button>
      </div>

    </div>
  );
}

export default App;