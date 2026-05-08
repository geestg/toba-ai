import { Link } from "react-router-dom";

export default function AboutPage() {
  const features = [
    {
      icon: "🤖",
      title: "Asisten AI Cerdas",
      desc: "Didukung oleh model bahasa besar (LLM) yang mampu memahami konteks dan memberikan rekomendasi personal.",
    },
    {
      icon: "📍",
      title: "Rekomendasi Lokasi",
      desc: "Saran destinasi berdasarkan lokasi real-time, kondisi cuaca, dan tingkat keramaian pengunjung.",
    },
    {
      icon: "🗺️",
      title: "Navigasi Rute",
      desc: "Integrasi peta interaktif untuk menampilkan rute perjalanan terbaik antar destinasi.",
    },
    {
      icon: "🍴",
      title: "Kuliner & Budaya",
      desc: "Informasi lengkap tentang makanan khas Batak, tradisi, dan pengalaman budaya autentik.",
    },
    {
      icon: "📅",
      title: "Itinerary Otomatis",
      desc: "Rencana perjalanan harian yang dioptimalkan berdasarkan waktu, jarak, dan preferensi pengguna.",
    },
    {
      icon: "🌙",
      title: "Mode Siang & Malam",
      desc: "Tampilan yang nyaman untuk mata dengan toggle mode terang dan gelap.",
    },
  ];

  const techStack = [
    { name: "React", role: "Frontend UI" },
    { name: "Vite", role: "Build Tool" },
    { name: "Leaflet", role: "Peta Interaktif" },
    { name: "Recharts", role: "Visualisasi Data" },
    { name: "FastAPI", role: "Backend API" },
    { name: "OpenStreetMap", role: "Data Geospasial" },
  ];

  return (
    <div className="about-page">
      {/* Hero */}
      <div className="about-hero">
        <div className="about-hero-content">
          <Link to="/" className="about-back">
            ← Kembali ke Chat
          </Link>
          <div className="about-hero-icon">🤖</div>
          <h1>Tentang AI Toba</h1>
          <p>
            AI Toba adalah asisten virtual pariwisata berbasis kecerdasan buatan yang
            didedikasikan untuk membantu wisatawan mengeksplorasi keindahan Danau Toba
            dan sekitarnya dengan lebih mudah, cerdas, dan personal.
          </p>
        </div>
      </div>

      {/* Mission */}
      <div className="about-section">
        <h2>🎯 Misi Kami</h2>
        <p className="about-mission-text">
          Mempermudah setiap wisatawan — baik lokal maupun mancanegara — untuk menemukan
          pengalaman terbaik di Danau Toba. Dari destinasi tersembunyi hingga kuliner
          legendaris, AI Toba hadir sebagai teman perjalanan digital yang selalu siap
          membantu kapan saja.
        </p>
      </div>

      {/* Features */}
      <div className="about-section">
        <h2>✨ Fitur Utama</h2>
        <div className="about-features-grid">
          {features.map((f, i) => (
            <div key={i} className="about-feature-card">
              <div className="about-feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="about-section">
        <h2>🛠️ Teknologi</h2>
        <div className="about-tech-grid">
          {techStack.map((t, i) => (
            <div key={i} className="about-tech-item">
              <strong>{t.name}</strong>
              <span>{t.role}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="about-section about-disclaimer">
        <h2>⚠️ Catatan Penting</h2>
        <p>
          AI Toba menggunakan model bahasa AI yang dapat menghasilkan informasi yang
          tidak selalu akurat. Informasi penting seperti harga tiket, jam operasional,
          dan kondisi jalan harap diverifikasi kembali melalui sumber resmi. Data lokasi
          dan rute bergantung pada ketersediaan layanan peta pihak ketiga.
        </p>
      </div>

      {/* Footer CTA */}
      <div className="about-cta">
        <p>Siap menjelajahi Danau Toba?</p>
        <Link to="/" className="about-cta-button">
          Mulai Chat dengan AI Toba →
        </Link>
      </div>
    </div>
  );
}

