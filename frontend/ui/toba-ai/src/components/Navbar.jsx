import { useState } from "react";

export default function Navbar({ onSetLocation }) {
  const [locating, setLocating] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const applyLocation = (latitude, longitude, message) => {
    onSetLocation?.({
      name: "Lokasi Saya",
      lat: latitude,
      lng: longitude,
    });
    setLocating(false);
    setStatusMessage(message);
  };

  const handleLocate = () => {
    if (!navigator.geolocation) {
      setStatusMessage("Browser tidak mendukung geolokasi. Aktifkan Location access di browser.");
      return;
    }

    setLocating(true);
    setStatusMessage("");

    if (navigator.permissions?.query) {
      navigator.permissions
        .query({ name: "geolocation" })
        .then((permission) => {
          if (permission.state === "denied") {
            setLocating(false);
            setStatusMessage("Izin lokasi diblokir. Aktifkan Location/Location access di Chrome.");
            return;
          }

          navigator.geolocation.getCurrentPosition(
            (position) => {
              applyLocation(position.coords.latitude, position.coords.longitude, "");
            },
            (error) => {
              console.error("GPS error:", error);
              setStatusMessage("Gagal mendapatkan lokasi. Periksa izin lokasi di browser.");
              setLocating(false);
            },
            { enableHighAccuracy: true, timeout: 10000 }
          );
        })
        .catch(() => {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              applyLocation(position.coords.latitude, position.coords.longitude, "");
            },
            (error) => {
              console.error("GPS error:", error);
              setStatusMessage("Gagal mendapatkan lokasi. Periksa izin lokasi di browser.");
              setLocating(false);
            },
            { enableHighAccuracy: true, timeout: 10000 }
          );
        });
    }
  };

  return (
    <div className="top-right-badge" aria-label="Aktifkan lokasi">
      {statusMessage && <div className="gps-status-message">{statusMessage}</div>}
      <button
        onClick={handleLocate}
        style={{
          background: "#fff",
          border: "1px solid #ccc",
          borderRadius: "50%",
          fontSize: "20px",
          width: "40px",
          height: "40px",
          cursor: "pointer",
          opacity: 1,
        }}
      >
        {locating ? "📡" : "📍"}
      </button>
    </div>
  );
}
