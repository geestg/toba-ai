export default function SystemFlow({ step }) {
  const steps = ["INPUT", "PLAN", "AGENTS", "ACTION"];

  return (
    <div className="flow">
      {steps.map((s, i) => (
        <div key={i} className={i + 1 <= step ? "active" : ""}>
          {s}
        </div>
      ))}
    </div>
  );
}