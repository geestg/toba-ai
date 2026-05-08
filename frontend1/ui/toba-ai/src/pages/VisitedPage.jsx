import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export default function VisitedPage() {
  const [visited, setVisited] = useState(() => {
    const saved = localStorage.getItem("toba-visited");
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem("toba-visited", JSON.stringify(visited));
  }, [visited]);

  const removeVisited = (name) => {
    setVisited((prev) => prev.filter((v) => v.name !== name));
  };

  const formatDate = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    return d.toLocaleDateString("id-ID", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const uniqueVisited = visited.filter(
    (v, i, self) => i === self.findIndex((t) => t.name === v.name)
  );

  return (
    <div className="favorites-page">
      {/* Header */}
      <div className="favorites-header">
        <div className="favorites-header-content">
          <Link to="/" className="favorites-back">
            ← Kembali ke Chat
          </Link>
          <h1>🗺️ Riwayat Kunjungan</h1>
          <p>Destinasi wisata yang pernah kamu pilih dan kunjungi.</p>
        </div>
      </div>

      {/* Stats */}
      {uniqueVisited.length > 0 && (
        <div style={{ padding: "0 24px 16px", color: "#4a5568", fontSize: "0.9rem" }}>
          Total <strong>{uniqueVisited.length}</strong> destinasi pernah dikunjungi
        </div>
      )}

      {/* Grid */}
      <div className="favorites-grid">
        {uniqueVisited.map((dest) => (
          <div key={dest.name} className="favorite-card">
            <div className="favorite-image-wrap">
              <img
                src={dest.image || `/images/${dest.name.toLowerCase().replace(/\s+/g, "").replace(/[^a-z0-9]/g, "")}.jpg`}
                alt={dest.name}
                loading="lazy"
                onError={(e) => { e.target.src = "/images/toba.jpg"; }}
              />
              <div className="favorite-overlay" />
              <button
                className="favorite-heart saved"
                onClick={() => removeVisited(dest.name)}
                title="Hapus dari riwayat"
              >
                🗑️
              </button>
              <div className="favorite-rating">
                <span>⭐</span>
                <span>{dest.rating ?? "-"}</span>
              </div>
            </div>
            <div className="favorite-info">
              <h3>{dest.name}</h3>
              <span className="favorite-saved-date">
                Dipilih {formatDate(dest.visitedAt)}
              </span>
              <div className="favorite-coords" style={{ marginTop: 6 }}>
                <span>📍</span>
                <span>{dest.area || "Danau Toba"}</span>
              </div>
              {dest.type && (
                <div style={{ marginTop: 4, fontSize: "0.8rem", color: "#718096" }}>
                  Tipe: <span style={{ textTransform: "capitalize" }}>{dest.type}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {uniqueVisited.length === 0 && (
        <div className="favorites-empty">
          <div className="empty-icon">🗺️</div>
          <h3>Belum ada riwayat kunjungan</h3>
          <p>Mulai pilih destinasi dari chat AI Toba, lalu datang kembali ke sini!</p>
          <Link to="/" className="empty-cta">
            Jelajahi Destinasi
          </Link>
        </div>
      )}
    </div>
  );
}

