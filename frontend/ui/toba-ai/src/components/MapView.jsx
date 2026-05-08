import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";

/* =========================================
   FIX DEFAULT LEAFLET ICON
========================================= */

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

/* =========================================
   START MARKER
========================================= */

const startIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",

  iconSize: [25, 41],

  iconAnchor: [12, 41],

  popupAnchor: [1, -34],

  shadowSize: [41, 41],
});

/* =========================================
   END MARKER
========================================= */

const endIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",

  iconSize: [25, 41],

  iconAnchor: [12, 41],

  popupAnchor: [1, -34],

  shadowSize: [41, 41],
});

/* =========================================
   COMPONENT
========================================= */

export default function MapView({
  route,
  startCoords,
  endCoords,
}) {
  let routeCoordinates = [];

  /* =========================================
     PARSE ROUTE FORMAT
  ========================================= */

  if (route) {
    if (Array.isArray(route)) {
      routeCoordinates = route;
    }

    else if (
      route.path &&
      Array.isArray(route.path)
    ) {
      // OSRM → [lng, lat]
      // Leaflet → [lat, lng]

      routeCoordinates = route.path.map(
        (coord) =>
          Array.isArray(coord) &&
          coord.length === 2
            ? [coord[1], coord[0]]
            : coord
      );
    }

    else if (
      route.coordinates &&
      Array.isArray(route.coordinates)
    ) {
      routeCoordinates = route.coordinates;
    }

    else if (
      route.geometry &&
      Array.isArray(route.geometry)
    ) {
      routeCoordinates = route.geometry;
    }
  }

  /* =========================================
     VALIDATE COORDINATES
  ========================================= */

  const validCoordinates =
    routeCoordinates.filter(
      (coord) =>
        Array.isArray(coord) &&
        coord.length === 2 &&
        typeof coord[0] === "number" &&
        typeof coord[1] === "number"
    );

  /* =========================================
     EMPTY STATE
  ========================================= */

  if (validCoordinates.length < 2) {
    return (
      <div className="map-empty-state">
        <span className="map-empty-icon">
          🗺️
        </span>

        <span className="map-empty-text">
          Peta rute tidak dapat ditampilkan
        </span>

        <small className="map-empty-sub">
          Koordinat valid:
          {" "}
          {validCoordinates.length}
        </small>
      </div>
    );
  }

  /* =========================================
     MAP CENTER
  ========================================= */

  const lats =
    validCoordinates.map((c) => c[0]);

  const lngs =
    validCoordinates.map((c) => c[1]);

  const centerLat =
    (Math.min(...lats) +
      Math.max(...lats)) /
    2;

  const centerLng =
    (Math.min(...lngs) +
      Math.max(...lngs)) /
    2;

  /* =========================================
     SMART ZOOM
  ========================================= */

  const latDiff =
    Math.max(...lats) -
    Math.min(...lats);

  const lngDiff =
    Math.max(...lngs) -
    Math.min(...lngs);

  const maxDiff =
    Math.max(latDiff, lngDiff);

  const zoom =
    maxDiff > 0.5
      ? 10
      : maxDiff > 0.1
      ? 12
      : 14;

  /* =========================================
     RENDER
  ========================================= */

  return (
    <div className="map-view-container">
      {/* AI OVERLAY */}
      <div className="map-ai-overlay">
        🤖 AI Redistribution Active
        <br />
        Crowd balancing & eco-routing enabled
      </div>

      {/* MAP */}
      <MapContainer
        center={[centerLat, centerLng]}
        zoom={zoom}
        style={{
          height: "240px",
          width: "100%",
          backgroundColor: "#f0f0f0",
        }}
        key={`map-${centerLat}-${centerLng}`}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

          maxZoom={19}

          minZoom={2}
        />

        {/* ROUTE */}
        {validCoordinates.length > 1 && (
          <Polyline
            positions={validCoordinates}
            color="#1fb7b7"
            weight={5}
            opacity={0.9}
            lineCap="round"
            lineJoin="round"
          />
        )}

        {/* START */}
        {startCoords &&
          typeof startCoords.lat ===
            "number" &&
          typeof startCoords.lng ===
            "number" && (
            <Marker
              position={[
                startCoords.lat,
                startCoords.lng,
              ]}
              icon={startIcon}
            >
              <Popup>
                📍 Titik Awal
              </Popup>
            </Marker>
          )}

        {/* DESTINATION */}
        {endCoords &&
          typeof endCoords.lat ===
            "number" &&
          typeof endCoords.lng ===
            "number" && (
            <Marker
              position={[
                endCoords.lat,
                endCoords.lng,
              ]}
              icon={endIcon}
            >
              <Popup>
                🏁 Destinasi Tujuan
              </Popup>
            </Marker>
          )}
      </MapContainer>

      {/* FOOTER */}
      <div className="map-footer">
        <div className="map-info">
          <div className="map-title">
            Smart Redistribution Route
          </div>

          <div className="map-subtitle">
            AI mengoptimalkan distribusi
            wisata berdasarkan crowd &
            environmental score
          </div>
        </div>

        <div className="map-status">
          ● Low Environmental Risk
        </div>
      </div>

      {/* LEGEND */}
      <div className="map-legend">
        <div className="map-legend-item">
          <span className="map-dot green"></span>

          Safe Area
        </div>

        <div className="map-legend-item">
          <span className="map-dot orange"></span>

          Moderate Crowd
        </div>

        <div className="map-legend-item">
          <span className="map-dot red"></span>

          High Density
        </div>
      </div>
    </div>
  );
}