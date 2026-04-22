export default function DecisionCard({ data }) {
  if (!data?.chosen) return null;

  return (
    <div className="decision-card">
      <h2>🎯 Rekomendasi AI</h2>

      <h3>{data.chosen.name}</h3>

      <p><b>Cuaca:</b> {data.weather.condition}</p>
      <p><b>Crowd:</b> {data.crowd.level} ({data.crowd.trend})</p>

      <div className="reasoning">
        {data.summary || "AI memilih lokasi ini berdasarkan kondisi optimal saat ini."}
      </div>
    </div>
  );
}