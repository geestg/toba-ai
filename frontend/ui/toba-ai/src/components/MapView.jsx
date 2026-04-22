import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView({ route }) {
  if (!route || route.length === 0) {
    return (
      <div style={{ height: "300px", display: "flex", alignItems: "center", justifyContent: "center", color: "#888" }}>
        Rute belum tersedia
      </div>
    );
  }

  return (
    <MapContainer
      center={route[0]}
      zoom={13}
      style={{ height: "220px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline positions={route} />
    </MapContainer>
  );
}