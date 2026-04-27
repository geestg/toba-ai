import MapView from "./MapView";

export default function RouteMap({ data }) {
  if (!data?.route) return null;

  const { distance, duration, geometry } = data.route;

  const distanceKm = distance
    ? (typeof distance === "number" ? distance / 1000 : parseFloat(distance)).toFixed(1)
    : "-";
  const durationMin = duration
    ? (typeof duration === "number" ? duration / 60 : parseFloat(duration)).toFixed(0)
    : "-";

  return (
    <div className="route-map-card animate-fade-in-up">
      <div className="route-map-header">
        <span>🗺️</span>
        <h3>Rute Perjalanan</h3>
      </div>

      <div className="route-map-stats">
        <div className="route-map-stat">
          <span className="route-map-stat-label">Jarak</span>
          <span className="route-map-stat-value">{distanceKm} km</span>
        </div>
        <div className="route-map-stat">
          <span className="route-map-stat-label">Durasi</span>
          <span className="route-map-stat-value">{durationMin} menit</span>
        </div>
        <div className="route-map-stat">
          <span className="route-map-stat-label">Moda</span>
          <span className="route-map-stat-value">🚗 Mobil</span>
        </div>
      </div>

      {geometry && (
        <div className="route-map-view">
          <MapView route={geometry} />
        </div>
      )}
    </div>
  );
}

