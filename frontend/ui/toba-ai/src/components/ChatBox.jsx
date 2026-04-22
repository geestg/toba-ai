import { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatBox({ onResult }) {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const handleSend = async () => {
    if (!message) return;

    const userMsg = { role: "user", text: message };
    setChat((prev) => [...prev, userMsg]);

    const res = await sendMessage(message);

    const botMsg = {
      role: "bot",
      text: res.reply,
      reasoning: res.reasoning,
    };

    setChat((prev) => [...prev, botMsg]);

    // 🔥 INI KUNCI
    if (onResult) onResult(res);

    setMessage("");
  };

  return (
    <div>
      <div className="chat-container">
        {chat.map((c, i) => (
          <div key={i} className={`bubble ${c.role}`}>
            {c.text}

            {c.reasoning && (
              <div className="reasoning">{c.reasoning}</div>
            )}
          </div>
        ))}
      </div>

      <div className="chat-bar">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Mau kemana hari ini..."
        />
        <button onClick={handleSend}>➤</button>
      </div>
    </div>
  );
}