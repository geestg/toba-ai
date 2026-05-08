export default function DecisionCard({ data }) {
  if (!data?.chosen) return null;

  const getWeatherIcon = (condition) => {
    const c = condition?.toLowerCase() || "";
    if (c.includes("hujan")) return "🌧️";
    if (c.includes("cerah")) return "☀️";
    if (c.includes("berawan")) return "☁️";
    return "🌤️";
  };

  const getCrowdColor = (level) => {
    const l = level?.toLowerCase() || "";
    if (l.includes("sepi")) return "#2f9a93";
    if (l.includes("ramai")) return "#f29b39";
    return "#8c5ae6";
  };

  return (
    <div className="decision-card animate-fade-in-scale">
      <div className="decision-header">
        <span className="decision-badge">🤖 AI Recommendation</span>
      </div>

      <h3 className="decision-title">{data.chosen.name}</h3>

      <div className="decision-stats">
        <div className="decision-stat">
          <span className="stat-icon">{getWeatherIcon(data.weather?.condition)}</span>
          <div>
            <span className="stat-label">Cuaca</span>
            <span className="stat-value">{data.weather?.condition || "Cerah"}</span>
          </div>
        </div>

        <div className="decision-stat">
          <span className="stat-icon" style={{ color: getCrowdColor(data.crowd?.level) }}>👥</span>
          <div>
            <span className="stat-label">Crowd</span>
            <span className="stat-value" style={{ color: getCrowdColor(data.crowd?.level) }}>
              {data.crowd?.level || "Normal"} ({data.crowd?.trend || "stable"})
            </span>
          </div>
        </div>
      </div>

      <div className="decision-reasoning">
        {data.summary || "AI memilih lokasi ini berdasarkan kondisi optimal saat ini."}
      </div>
    </div>
  );
}

