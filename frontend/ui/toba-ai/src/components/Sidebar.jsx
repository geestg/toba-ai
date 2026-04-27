import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import Logo from "./Logo";

export default function Sidebar({ isOpen, onToggle, themeMode, onToggleTheme, gpsActive, location, onToggleGPS }) {
  const [locating, setLocating] = useState(false);
  const currentPath = useLocation().pathname;

  const handleEnableGPS = () => {
    if (!navigator.geolocation) {
      alert("Browser tidak mendukung geolokasi.");
      return;
    }

    setLocating(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        onToggleGPS?.({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
        setLocating(false);
      },
      (error) => {
        console.error("GPS error:", error);
        alert("Gagal mendapatkan lokasi. Pastikan izin lokasi diaktifkan.");
        setLocating(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const menuItems = [
    { icon: "💬", label: "Chat dengan AI Toba", path: "/" },
    { icon: "♡", label: "Favorit", path: "/favorites" },
    { icon: "ℹ", label: "Tentang AI Toba", path: "/about" },
  ];

  return (
    <aside className={`sidebar-fixed ${isOpen ? "is-open" : "is-closed"}`}>
      <div className="sidebar-brand" onClick={!isOpen ? onToggle : undefined} role={!isOpen ? "button" : undefined} tabIndex={!isOpen ? 0 : -1} aria-label={!isOpen ? "Buka sidebar" : undefined}>
        <div className="brand-mark-svg">
          <Logo size={38} />
        </div>
        {isOpen && (
          <div className="brand-text">
            <h1>AI Toba</h1>
            <p>AI Agent Pariwisata Danau Toba</p>
          </div>
        )}
        {isOpen && (
          <button
            type="button"
            className="sidebar-collapse-btn"
            onClick={onToggle}
            aria-label="Tutup sidebar"
          >
            ◀
          </button>
        )}
      </div>

      {isOpen && (
        <>
          <nav className="sidebar-nav">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`sidebar-link ${currentPath === item.path ? "active" : ""}`}
              >
                <span className="sidebar-link-icon">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          <div className="sidebar-history">
            <span className="sidebar-history-title">RIWAYAT TERBARU</span>
            <div className="sidebar-history-item">
              <span className="history-text">"Sunset terbaik di Samosir"</span>
              <span className="history-time">10:30</span>
            </div>
            <div className="sidebar-history-item">
              <span className="history-text">"Kuliner khas Batak"</span>
              <span className="history-time">Kemarin</span>
            </div>
            <div className="sidebar-history-item">
              <span className="history-text">"Rekomendasi 2 hari 1 malam"</span>
              <span className="history-time">Kemarin</span>
            </div>
            <div className="sidebar-history-item">
              <span className="history-text">"Transportasi ke Danau Toba"</span>
              <span className="history-time">2 hari lalu</span>
            </div>
            <div className="sidebar-history-item">
              <span className="history-text">"Tips liburan di Danau Toba"</span>
              <span className="history-time">3 hari lalu</span>
            </div>
          </div>

          <div className="sidebar-agent-card">
            <div className="sidebar-art">
              <img src="/images/toba.jpg" alt="Danau Toba" />
            </div>
            <h4>AI Toba</h4>
            <p>
              Asisten virtual pariwisata
              <br />
              Danau Toba siap membantu
              <br />
              merencanakan perjalananmu!
            </p>

            <div className="sidebar-gps-row">
              <button
                type="button"
                className={`sidebar-mode-row sidebar-mode-button ${gpsActive ? "gps-active" : ""}`}
                onClick={handleEnableGPS}
                disabled={locating}
              >
                <span>{locating ? "📡" : "📍"}</span>
                <span className="gps-label">
                  {locating ? "Mencari lokasi..." : gpsActive ? "GPS Aktif" : "Aktifkan Lokasi"}
                </span>
                <span>▾</span>
              </button>

              {gpsActive && location && (
                <div className="gps-coords">
                  Lat: {location.lat.toFixed(4)}, Lng: {location.lng.toFixed(4)}
                </div>
              )}
            </div>

            <button type="button" className="sidebar-mode-row sidebar-mode-button" onClick={onToggleTheme}>
              <span>{themeMode === "siang" ? "☼" : "☾"}</span>
              <span>{themeMode === "siang" ? "Mode Siang" : "Mode Malam"}</span>
              <span>▾</span>
            </button>

            <div className="sidebar-profile-row">
              <img src="https://i.pravatar.cc/40?img=44" alt="Dora Imut" />
              <div>
                <strong>Dora Imut</strong>
                <small>dora.imut@email.com</small>
              </div>
              <span>▾</span>
            </div>
          </div> 
        </>
      )}
    </aside>
  );
}

