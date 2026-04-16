import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

export default function MapView({ locations }) {
  const getColor = (c) => {
    if (c > 75) return "red";
    if (c > 50) return "orange";
    return "green";
  };

  return (
    <MapContainer center={[2.6, 98.9]} zoom={10} style={{ height: "400px" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {locations.map((loc, i) => (
        <CircleMarker
          key={i}
          center={[2.6 + i * 0.02, 98.9 + i * 0.02]}
          radius={10}
          pathOptions={{ color: getColor(loc.simulated_crowd) }}
        >
          <Popup>
            {loc.name}
            <br />
            Crowd: {loc.simulated_crowd}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}