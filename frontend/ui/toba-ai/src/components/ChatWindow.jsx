import { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatWindow({ setData, setLoading }) {
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input) return;

    setLoading(true);

    try {
      const res = await sendMessage(input);
      setData(res.data);
    } catch (e) {
      console.error(e);
    }

    setLoading(false);
  };

  return (
    <div className="chat">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Mau kemana nich?"
      />
      <button onClick={handleSend}>Cari</button>
    </div>
  );
}