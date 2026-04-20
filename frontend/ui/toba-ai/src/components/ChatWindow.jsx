import { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatWindow({ setData, setLoading }) {
  const [input, setInput] = useState("");

  const handleSend = async () => {
    setLoading(true);
    try {
      const res = await sendMessage(input);
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Mau kemana?"
      />
      <button onClick={handleSend}>Kirim</button>
    </div>
  );
}