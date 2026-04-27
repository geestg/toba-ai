import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { destinations } from "../data/destinations";

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState(() => {
    const saved = localStorage.getItem("toba-favorites");
    return saved ? JSON.parse(saved) : [];
  });

  const [activeTab, setActiveTab] = useState("all");

  useEffect(() => {
    localStorage.setItem("toba-favorites", JSON.stringify(favorites));
  }, [favorites]);

  const toggleFavorite = (dest) => {
    setFavorites((prev) => {
      const exists = prev.find((f) => f.name === dest.name);
      if (exists) {
        return prev.filter((f) => f.name !== dest.name);
      }
      return [...prev, { ...dest, savedAt: new Date().toISOString() }];
    });
  };

  const isFavorited = (name) => favorites.some((f) => f.name === name);

  const filteredDestinations =
    activeTab === "saved"
      ? destinations.filter((d) => isFavorited(d.name))
      : destinations;

  const formatDate = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    return d.toLocaleDateString("id-ID", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="favorites-page">
      {/* Header */}
      <div className="favorites-header">
        <div className="favorites-header-content">
          <Link to="/" className="favorites-back">
            ← Kembali ke Chat
          </Link>
          <h1>⭐ Favorit Saya</h1>
          <p>Simpan dan kelola destinasi, kuliner, dan tips wisata favoritmu.</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="favorites-tabs">
        <button
          className={activeTab === "all" ? "active" : ""}
          onClick={() => setActiveTab("all")}
        >
          Semua Destinasi
          <span className="tab-count">{destinations.length}</span>
        </button>
        <button
          className={activeTab === "saved" ? "active" : ""}
          onClick={() => setActiveTab("saved")}
        >
          Tersimpan
          <span className="tab-count">{favorites.length}</span>
        </button>
      </div>

      {/* Grid */}
      <div className="favorites-grid">
        {filteredDestinations.map((dest) => {
          const saved = favorites.find((f) => f.name === dest.name);
          return (
            <div key={dest.name} className="favorite-card">
              <div className="favorite-image-wrap">
                <img src={dest.img} alt={dest.name} loading="lazy" />
                <div className="favorite-overlay" />
                <button
                  className={`favorite-heart ${isFavorited(dest.name) ? "saved" : ""}`}
                  onClick={() => toggleFavorite(dest)}
                  title={isFavorited(dest.name) ? "Hapus dari favorit" : "Tambah ke favorit"}
                >
                  {isFavorited(dest.name) ? "♥" : "♡"}
                </button>
                <div className="favorite-rating">
                  <span>⭐</span>
                  <span>{dest.rating}</span>
                </div>
              </div>
              <div className="favorite-info">
                <h3>{dest.name}</h3>
                {saved && (
                  <span className="favorite-saved-date">
                    Disimpan {formatDate(saved.savedAt)}
                  </span>
                )}
                <div className="favorite-coords">
                  <span>📍</span>
                  <span>
                    {dest.coords.lat.toFixed(3)}, {dest.coords.lng.toFixed(3)}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredDestinations.length === 0 && (
        <div className="favorites-empty">
          <div className="empty-icon">♡</div>
          <h3>Belum ada favorit</h3>
          <p>Mulai simpan destinasi menarik dari chat AI Toba!</p>
          <Link to="/" className="empty-cta">
            Jelajahi Destinasi
          </Link>
        </div>
      )}
    </div>
  );
}

