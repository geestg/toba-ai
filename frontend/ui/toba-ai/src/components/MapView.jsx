import { MapContainer, TileLayer, Marker, Polyline, useMap } from "react-leaflet";
import { useEffect, useState } from "react";
import "leaflet/dist/leaflet.css";

// auto zoom component
function AutoZoom({ route }) {
  const map = useMap();

  useEffect(() => {
    if (route && route.length > 0) {
      map.fitBounds(route, { padding: [50, 50] });
    }
  }, [route]);

  return null;
}

function MapView({ route }) {
  const [animatedRoute, setAnimatedRoute] = useState([]);

  useEffect(() => {
    if (!route) return;

    let i = 0;
    setAnimatedRoute([]);

    const interval = setInterval(() => {
      setAnimatedRoute((prev) => [...prev, route[i]]);
      i++;
      if (i >= route.length) clearInterval(interval);
    }, 200); // speed animasi

    return () => clearInterval(interval);
  }, [route]);

  if (!route) return null;

  return (
    <MapContainer
      center={route[0]}
      zoom={13}
      style={{
        height: "300px",
        margin: "20px",
        borderRadius: "20px",
      }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <AutoZoom route={route} />

      <Polyline positions={animatedRoute} color="cyan" />

      <Marker position={route[0]} />
      <Marker position={route[route.length - 1]} />
    </MapContainer>
  );
}

export default MapView;