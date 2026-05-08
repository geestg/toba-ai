import { useState } from "react";

export default function Navbar({ onSetLocation }) {
  const [locating, setLocating] = useState(false);

  const handleLocate = () => {
    if (!navigator.geolocation) {
      alert("Browser tidak mendukung geolokasi.");
      return;
    }

    setLocating(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        onSetLocation?.({
          name: "Lokasi Saya",
          lat: latitude,
          lng: longitude,
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

  return (
    <div className="top-right-badge" aria-label="Aktifkan lokasi">
        <button
    onClick={handleLocate}
    style={{
      background: "#fff", // ubah ke putih supaya kontras
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
