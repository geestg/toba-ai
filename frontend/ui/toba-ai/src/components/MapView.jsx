import { MapContainer, TileLayer, Marker } from "react-leaflet";

export default function MapView({ data }) {
  if (!data) return null;

  const loc = data.decision.final_decision;

  return (
    <MapContainer center={[loc.lat, loc.lng]} zoom={10} style={{ height: "300px" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[loc.lat, loc.lng]} />
    </MapContainer>
  );
}