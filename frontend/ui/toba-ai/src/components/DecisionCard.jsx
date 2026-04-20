export default function DecisionCard({ decision }) {
  if (!decision) return null;

  return (
    <div className="card glow">
      <h2>Final Decision</h2>
      <p><strong>Lokasi:</strong> {decision.final_decision.name}</p>
      <p><strong>Score:</strong> {decision.score}</p>
      <p>{decision.reason}</p>
    </div>
  );
}