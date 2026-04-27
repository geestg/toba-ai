export default function UMKMPanel({ data }) {
  if (!data?.umkm) return null;

  const categoryColors = [
    { bg: "#e7f8f5", text: "#2f9a93", border: "#b8e8e0" },
    { bg: "#ecf4ff", text: "#2f8dea", border: "#c2d8f9" },
    { bg: "#fff2e7", text: "#f29b39", border: "#f5d6b8" },
    { bg: "#f1eaff", text: "#8c5ae6", border: "#d8c8f5" },
  ];

  return (
    <div className="umkm-panel animate-fade-in-up">
      <div className="umkm-header">
        <span className="umkm-icon">🏪</span>
        <h3>Peluang UMKM</h3>
      </div>

      <div className="umkm-grid">
        {data.umkm.map((u, i) => {
          const color = categoryColors[i % categoryColors.length];
          return (
            <div
              key={i}
              className="umkm-card"
              style={{
                borderLeftColor: color.border,
                background: `linear-gradient(135deg, ${color.bg} 0%, #fff 100%)`,
              }}
            >
              <h4 style={{ color: color.text }}>{u.name}</h4>
              <ul>
                {u.opportunities.map((o, j) => (
                  <li key={j}>{o}</li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}

