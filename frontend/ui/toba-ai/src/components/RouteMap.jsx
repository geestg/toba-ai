import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import { useEffect, useState } from "react";
import "leaflet/dist/leaflet.css";

export default function RouteMap({ route }) {
  const [progressIndex, setProgressIndex] = useState(0);

  if (!route) return null;

  const start = [route.start.lat, route.start.lng];
  const end = [route.end[0], route.end[1]];


  const path = route.path.map((p) => [p[1], p[0]]);

  useEffect(() => {
    let i = 0;

    const interval = setInterval(() => {
      i++;
      if (i >= path.length - 1) clearInterval(interval);
      setProgressIndex(i);
    }, 30);

    return () => clearInterval(interval);
  }, [route]);

  const currentPosition = path[progressIndex] || start;

  return (
    <div className="map">
      <MapContainer
        center={start}
        zoom={11}
        style={{ height: "400px", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {/* Start */}
        <Marker position={start} />

        {/* Moving marker */}
        <Marker position={currentPosition} />

        {/* End */}
        <Marker position={end} />

        {/* Real path */}
        <Polyline positions={path} />
      </MapContainer>
    </div>
  );
}