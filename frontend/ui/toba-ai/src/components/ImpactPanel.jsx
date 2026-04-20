export default function ImpactPanel({ impact }) {
  return (
    <div className="impact">
      <h2>Impact Analysis</h2>

      <p> Environment: {impact.environment}</p>
      <p> Economic: {impact.economic}</p>
    </div>
  );
}