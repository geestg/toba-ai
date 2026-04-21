import { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatBox({ setResponse }) {
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input) return;

    const position = await new Promise((res) =>
      navigator.geolocation.getCurrentPosition(res)
    );

    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    const result = await sendMessage(input, lat, lng);

    setResponse(result);
    setInput("");
  };

  return (
    <div className="chat">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Mau kemana hari ini?"
      />
      <button onClick={handleSend}>Kirim</button>
    </div>
  );
}