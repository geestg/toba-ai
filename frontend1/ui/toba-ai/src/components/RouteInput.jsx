import { useState } from "react";
import { getRoute } from "../services/api";

export default function RouteInput({ onRouteFound }) {
  const [startLocation, setStartLocation] = useState("");
  const [endLocation, setEndLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [routeInfo, setRouteInfo] = useState(null);

  const exampleLocations = {
    "medan center": { lat: 2.19729, lng: 98.66521 },
    "berastagi": { lat: 2.96833, lng: 98.51833 },
    "sibayak": { lat: 2.95, lng: 98.5 },
    "tip top": { lat: 2.18956, lng: 98.67428 },
    "merdeka": { lat: 2.20559, lng: 98.67003 },
    "polda": { lat: 2.19945, lng: 98.68087 },
    "holbung": { lat: 2.33, lng: 98.88 },
    "parbaba": { lat: 2.32, lng: 98.92 },
  };

  const parseLocation = (locationString) => {
    const normalized = locationString.toLowerCase().trim();
    if (exampleLocations[normalized]) {
      return exampleLocations[normalized];
    }

    const coordMatch = locationString.match(
      /(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)/
    );
    if (coordMatch) {
      return {
        lat: parseFloat(coordMatch[1]),
        lng: parseFloat(coordMatch[2]),
      };
    }

    throw new Error(
      `Lokasi "${locationString}" tidak ditemukan. Coba: ${Object.keys(exampleLocations).join(", ")} atau koordinat (lat,lng)`
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setRouteInfo(null);

    if (!startLocation.trim() || !endLocation.trim()) {
      setError("Kedua lokasi harus diisi!");
      return;
    }

    try {
      setLoading(true);

      const startCoords = parseLocation(startLocation);
      const endCoords = parseLocation(endLocation);

      const routeData = await getRoute(startCoords, endCoords);

      if (!routeData.routes || routeData.routes.length === 0) {
        throw new Error("Rute tidak ditemukan");
      }

      const route = routeData.routes[0];
      const distance = (route.summary.distance / 1000).toFixed(2);
      const duration = Math.round(route.summary.duration / 60);

      setRouteInfo({
        distance,
        duration,
        startCoords,
        endCoords,
      });

      if (onRouteFound) {
        onRouteFound({
          route: routeData.routes[0],
          distance,
          duration,
        });
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="route-panel animate-fade-in-up">
      <div className="route-panel-header">
        <span className="route-panel-icon">🗺️</span>
        <h3>Cari Rute Perjalanan</h3>
      </div>

      <form onSubmit={handleSubmit} className="route-form">
        <div className="route-input-group">
          <label htmlFor="start">Dari</label>
          <input
            id="start"
            type="text"
            placeholder="Contoh: Medan Center atau 2.1945,98.6722"
            value={startLocation}
            onChange={(e) => setStartLocation(e.target.value)}
            disabled={loading}
          />
        </div>

        <div className="route-divider">
          <span>↓</span>
        </div>

        <div className="route-input-group">
          <label htmlFor="end">Ke</label>
          <input
            id="end"
            type="text"
            placeholder="Contoh: Holbung atau 2.33,98.88"
            value={endLocation}
            onChange={(e) => setEndLocation(e.target.value)}
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading} className="route-submit-btn">
          {loading ? (
            <>
              <span className="spinner animate-spin">⟳</span>
              Mencari rute...
            </>
          ) : (
            "🔍 Cari Rute"
          )}
        </button>
      </form>

      {error && (
        <div className="route-error">
          <span>⚠️</span> {error}
        </div>
      )}

      {routeInfo && (
        <div className="route-result animate-fade-in-scale">
          <h4>✅ Rute Ditemukan</h4>
          <div className="route-result-stats">
            <div className="route-stat">
              <span className="route-stat-label">Jarak</span>
              <span className="route-stat-value">{routeInfo.distance} km</span>
            </div>
            <div className="route-stat">
              <span className="route-stat-label">Durasi</span>
              <span className="route-stat-value">{routeInfo.duration} menit</span>
            </div>
          </div>
          <div className="route-result-coords">
            Dari: ({routeInfo.startCoords.lat.toFixed(4)}, {routeInfo.startCoords.lng.toFixed(4)})
            <br />
            Ke: ({routeInfo.endCoords.lat.toFixed(4)}, {routeInfo.endCoords.lng.toFixed(4)})
          </div>
        </div>
      )}

      <div className="route-examples">
        <p className="route-examples-title">📍 Contoh lokasi:</p>
        <div className="route-example-tags">
          {Object.keys(exampleLocations).map((loc) => (
            <button
              key={loc}
              className="route-example-tag"
              onClick={() => setStartLocation(loc)}
              type="button"
            >
              {loc}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

