import "./App.css";
import { useState, useRef } from "react";
import { destinations } from "./data/destinations";
import MapView from "./components/MapView";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [selected, setSelected] = useState(null);
  const [route, setRoute] = useState(null);
  const [typingText, setTypingText] = useState("");

  const scrollRef = useRef(null);

  // 🔥 AUTO SCROLL KE DESTINASI
  const scrollToDestination = (name) => {
    const index = destinations.findIndex((d) => d.name === name);
    if (index === -1) return;

    const cardWidth = 240;
    scrollRef.current.scrollTo({
      left: index * cardWidth,
      behavior: "smooth",
    });
  };

  // 🔥 TYPING EFFECT
  const typeText = (text) => {
    let i = 0;
    setTypingText("");

    const interval = setInterval(() => {
      i++;
      setTypingText(text.slice(0, i));
      if (i >= text.length) clearInterval(interval);
    }, 15);
  };

  // 🔥 SEND MESSAGE
  const sendMessage = async (customText) => {
    const text = customText || input;
    if (!text) return;

    setMessages((prev) => [...prev, { role: "user", text }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await res.json();

      // SET DESTINATION
      if (data.data?.chosen) {
        setSelected(data.data.chosen);
        scrollToDestination(data.data.chosen.name);
      }

      // SET ROUTE
      if (data.data?.route) {
        setRoute(data.data.route);
      }

      // typing effect
      typeText(data.reply);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.reply,
          decision: data.data?.chosen,
          impact: data.data?.impact,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Server error, cek backend mu bos." },
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

      {/* 🔥 MAP (HANYA MUNCUL KALAU ADA ROUTE) */}
      {route && (
        <div style={{ height: "400px", margin: "20px" }}>
          <MapView route={route} />
        </div>
      )}

      {/* DECISION */}
      {selected && (
        <div className="decision-highlight">
          <h2>{selected.name}</h2>
          <p>Dipilih berdasarkan AI analysis</p>
        </div>
      )}

      {/* SECTION TITLE */}
      <div className="section">
        <h2>Destinasi Populer</h2>
        <p>Udah Kemana aja lek?</p>
      </div>

      {/* DESTINATION */}
      <div className="destination-wrapper">
        <div className="card-container" ref={scrollRef}>
          {destinations.map((d, i) => (
            <div
              key={i}
              className={`card ${
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

      {/* CHAT */}
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble ${msg.role}`}>
            <p>
              {i === messages.length - 1 && msg.role === "bot"
                ? typingText
                : msg.text}
            </p>

            {msg.decision && (
              <div className="decision-box">
                AI pilih: {msg.decision.name}
              </div>
            )}

            {msg.impact && (
              <div className="impact-box">
                Crowd: {msg.impact?.before} → {msg.impact?.after}
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
          placeholder="Mau kemana hari ini lekku..."
        />
        <button onClick={() => sendMessage()}>➤</button>
      </div>

    </div>
  );
}

export default App;