import { destinations } from "../data/destinations";

export default function DestinationCarousel() {
  return (
    <section className="destination-section">
      <div className="section-header">
        <h2 className="section-title">✨ Destinasi Wisata Populer</h2>
        <p className="section-subtitle">Temukan keindahan tersembunyi di sekitar Danau Toba</p>
      </div>

      <div className="destination-grid">
        {destinations.map((d, i) => (
          <div key={i} className="destination-card animate-fade-in-up" style={{ animationDelay: `${i * 0.06}s` }}>
            <div className="destination-image-wrap">
              <img src={d.img || d.image} alt={d.name} loading="lazy" />
              <div className="destination-image-overlay" />
              <div className="destination-badge">
                <span>⭐</span>
                <span>{d.rating}</span>
              </div>
            </div>

            <div className="destination-card-content">
              <h3>{d.name}</h3>
              <div className="destination-meta">
                <span className="destination-coords">
                  📍 {d.coords.lat.toFixed(2)}, {d.coords.lng.toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

