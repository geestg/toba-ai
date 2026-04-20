export default function AgentFlow() {
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

  return (
    <div className="flow">
      {agents.map((a, i) => (
        <div key={i} className="agent">
          {a}
        </div>
      ))}
    </div>
  );
}