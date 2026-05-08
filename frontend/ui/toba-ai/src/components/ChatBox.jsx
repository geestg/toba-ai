import { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatBox({ onResult }) {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };
    setChat((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await sendMessage(message);

      const botMsg = {
        role: "bot",
        text: res.reply,
        reasoning: res.reasoning,
      };

      setChat((prev) => [...prev, botMsg]);

      if (onResult) onResult(res);
    } catch {
      setChat((prev) => [
        ...prev,
        { role: "bot", text: "Maaf, terjadi kesalahan. Silakan coba lagi. 🙏" },
      ]);
    } finally {
      setIsLoading(false);
      setMessage("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chatbox-wrapper">
      <div className="chatbox-messages">
        {chat.map((c, i) => (
          <div key={i} className={`chatbox-row ${c.role}`}>
            {c.role === "bot" && (
              <div className="chatbox-avatar bot">✦</div>
            )}
            <div className="chatbox-bubble-wrapper">
              <div className="chatbox-bubble">{c.text}</div>
              {c.reasoning && (
                <div className="chatbox-reasoning">{c.reasoning}</div>
              )}
            </div>
            {c.role === "user" && (
              <div className="chatbox-avatar user">👤</div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="chatbox-row bot">
            <div className="chatbox-avatar bot">✦</div>
            <div className="chatbox-bubble typing">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        )}
      </div>

      <div className="chatbox-input-bar">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Mau kemana hari ini..."
          aria-label="Pesan ke AI Toba"
        />
        <button
          onClick={handleSend}
          disabled={!message.trim() || isLoading}
          aria-label="Kirim pesan"
        >
          ➤
        </button>
      </div>
    </div>
  );
}

