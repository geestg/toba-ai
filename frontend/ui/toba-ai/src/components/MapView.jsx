import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const locations = [
  { name: "Parapat", lat: 2.663, lng: 98.934 },
  { name: "Samosir", lat: 2.604, lng: 98.699 },
  { name: "Balige", lat: 2.333, lng: 99.067 },
  { name: "Sipinsur", lat: 2.408, lng: 98.913 }
];

export default function MapView({ decision }) {
  if (!decision) return null;

  const best = decision.final_decision.name;

  return (
    <div className="card">
      <h3>Tourism Map</h3>
      <MapContainer center={[2.6, 98.9]} zoom={10} style={{ height: "300px" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {locations.map((loc, i) => (
          <Marker key={i} position={[loc.lat, loc.lng]}>
            <Popup>
              {loc.name} {loc.name === best ? "⭐ Recommended" : ""}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}