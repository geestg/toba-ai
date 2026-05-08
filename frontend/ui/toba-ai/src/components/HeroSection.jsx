export default function HeroSection() {

  return (
    <section className="hero-section">

      {/* ===================== */}
      {/* BACKGROUND */}
      {/* ===================== */}

      <img
        src="/images/toba-hero.jpg"
        alt="Danau Toba"
        className="hero-image"
      />

      <div className="hero-overlay" />

      {/* ===================== */}
      {/* CONTENT */}
      {/* ===================== */}

      <div className="hero-content animate-fade-up">

        <span className="hero-badge">
          AI Tourism Assistant
        </span>

        <h1 className="hero-title">
          Jelajahi Danau Toba
          <br />
          Dengan Rekomendasi AI
        </h1>

        <p className="hero-description">
          Sistem rekomendasi wisata berbasis AI
          untuk membantu perjalanan yang lebih
          nyaman, personal, dan relevan berdasarkan
          kondisi wisata secara real-time.
        </p>

        {/* ===================== */}
        {/* STATS */}
        {/* ===================== */}

        <div className="hero-stats">

          <div className="hero-stat-card">

            <strong>70+</strong>

            <span>Destinasi</span>

          </div>

          <div className="hero-stat-card">

            <strong>AI</strong>

            <span>Recommendation</span>

          </div>

          <div className="hero-stat-card">

            <strong>Smart</strong>

            <span>Travel Routing</span>

          </div>

        </div>

      </div>

    </section>
  );
}