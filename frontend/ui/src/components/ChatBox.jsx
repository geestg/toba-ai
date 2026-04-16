import { useState } from "react";

export default function ChatBox({ onSend }) {
  const [text, setText] = useState("");

  return (
    <div className="control">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Mau kemana?"
      />
      <button
        className="btn"
        onClick={() => {
          onSend(text);
          setText("");
        }}
      >
        Ask AI
      </button>
    </div>
  );
}