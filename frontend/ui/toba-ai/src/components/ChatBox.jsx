import { useEffect, useRef, useState } from "react";

import { sendMessage } from "../services/api";


export default function ChatBox({ onResult }) {

  const [message, setMessage] = useState("");

  const [chat, setChat] = useState([]);

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);


  // =====================================
  // AUTO SCROLL
  // =====================================

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [chat, loading]);


  // =====================================
  // SEND MESSAGE
  // =====================================

  async function handleSend() {

    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      text: message,
    };

    setChat((prev) => [
      ...prev,
      userMessage,
    ]);

    setLoading(true);

    const res = await sendMessage(message);

    const botMessage = {
      role: "bot",
      text: res.reply,
    };

    setChat((prev) => [
      ...prev,
      botMessage,
    ]);

    if (onResult) {
      onResult(res);
    }

    setMessage("");

    setLoading(false);
  }


  // =====================================
  // ENTER SEND
  // =====================================

  function handleKeyDown(e) {

    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {

      e.preventDefault();

      handleSend();
    }
  }


  return (

    <section className="chat-section">

      {/* ===================== */}
      {/* HEADER */}
      {/* ===================== */}

      <div className="chat-header animate-fade-up">

        <div>

          <span className="chat-mini-label">
            Smart AI Assistant
          </span>

          <h2 className="chat-title">
            Rencanakan perjalanan Anda
          </h2>

        </div>

        <div className="chat-status">
          Online
        </div>

      </div>

      {/* ===================== */}
      {/* CHAT CONTAINER */}
      {/* ===================== */}

      <div className="chatbox-wrapper">

        <div className="chatbox-messages">

          {chat.length === 0 && (

            <div className="chat-welcome animate-fade-up">

              <h3>
                Mulai perjalanan wisata Anda
              </h3>

              <p>
                Coba tanyakan rekomendasi wisata,
                kuliner, penginapan, atau rute
                perjalanan di sekitar Danau Toba.
              </p>

            </div>
          )}

          {chat.map((item, index) => (

            <div
              key={index}
              className={`chatbox-row ${item.role}`}
            >

              {item.role === "bot" && (

                <div className="chat-avatar bot">
                  AI
                </div>
              )}

              <div className="chatbox-bubble animate-message">

                {item.text}

              </div>

              {item.role === "user" && (

                <div className="chat-avatar user">
                  U
                </div>
              )}

            </div>
          ))}

          {loading && (

            <div className="chatbox-row bot">

              <div className="chat-avatar bot">
                AI
              </div>

              <div className="chatbox-bubble typing-bubble">

                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />

              </div>

            </div>
          )}

          <div ref={bottomRef} />

        </div>

        {/* ===================== */}
        {/* INPUT */}
        {/* ===================== */}

        <div className="chatbox-input-shell">

          <div className="chatbox-input-bar">

            <input
              type="text"
              placeholder="Cari rekomendasi wisata terbaik..."
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={handleKeyDown}
            />

            <button onClick={handleSend}>
              →
            </button>

          </div>

        </div>

      </div>

    </section>
  );
}