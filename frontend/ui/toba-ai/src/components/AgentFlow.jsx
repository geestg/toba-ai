import { useEffect, useState } from "react";

const agents = [
  "Intent",
  "Planner",
  "Environment",
  "Routing",
  "Cost",
  "Weather",
  "UMKM",
  "Decision"
];

export default function AgentFlow({ trigger }) {
  const [active, setActive] = useState(-1);

  useEffect(() => {
    if (!trigger) return;

    let i = 0;
    const interval = setInterval(() => {
      setActive(i);
      i++;
      if (i >= agents.length) clearInterval(interval);
    }, 400);

    return () => clearInterval(interval);
  }, [trigger]);

  return (
    <div className="card">
      <h3>Agent Flow</h3>
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
        {agents.map((a, i) => (
          <div
            key={i}
            style={{
              padding: "10px",
              borderRadius: "8px",
              background: i === active ? "#38bdf8" : "#334155",
              color: i === active ? "#0f172a" : "#e2e8f0",
              transition: "0.3s"
            }}
          >
            {a}
          </div>
        ))}
      </div>
    </div>
  );
}