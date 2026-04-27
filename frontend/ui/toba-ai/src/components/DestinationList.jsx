export default function DestinationList({ data }) {
  if (!data?.destinations) return null;

  return (
    <section className="destination-section">
      <div className="section-header">
        <h2 className="section-title">🎯 Hasil Rekomendasi</h2>
      </div>

      <div className="destination-grid">
        {data.destinations.map((d, i) => (
          <div key={i} className="destination-card animate-fade-in-up" style={{ animationDelay: `${i * 0.06}s` }}>
            <div className="destination-image-wrap">
              <img src={d.image} alt={d.name} loading="lazy" />
              <div className="destination-image-overlay" />
              <div className="destination-badge">
                <span>⭐</span>
                <span>{d.rating}</span>
              </div>
            </div>

            <div className="destination-card-content">
              <h3>{d.name}</h3>
              {d.description && (
                <p className="destination-desc">{d.description}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

