export default function ImpactPanel({ impact }) {
  if (!impact) return null;

  return (
    <div className="card">
      <h3>Impact Analysis</h3>

      <p>Avg Crowd: {impact.environment.avg_crowd}</p>
      <p>Crowd Reduction: {impact.environment.crowd_reduction}</p>

      <p>UMKM Boost: {impact.economic.umkm_boost_score}</p>
    </div>
  );
}