export async function sendMessage(message) {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      lat: -2.5,
      lng: 99.1,
    }),
  });

  return res.json();
}

/* =========================================
   Routing APIs
   ========================================= */

// Simple polyline decoder (RFC 4648)
function decodePolyline(encoded) {
  const points = [];
  let index = 0, lat = 0, lng = 0;

  while (index < encoded.length) {
    let b, shift = 0, result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    const dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lat += dlat;

    shift = 0;
    result = 0;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    const dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lng += dlng;

    points.push([lat / 1e5, lng / 1e5]);
  }
  return points;
}

// OSRM Routing (open source, wide coverage)
export async function getRouteOSRM(startCoords, endCoords) {
  try {
    const url = `https://router.project-osrm.org/route/v1/driving/${startCoords.lng},${startCoords.lat};${endCoords.lng},${endCoords.lat}?overview=full&steps=true&geometries=geojson`;
    console.log("OSRM URL:", url);

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`OSRM error: ${response.status}`);
    }

    const data = await response.json();
    console.log("OSRM response:", data);

    if (data.code !== "Ok" || !data.routes || data.routes.length === 0) {
      throw new Error(`OSRM: ${data.message || "Route not found"}`);
    }

    const route = data.routes[0];
    let routeCoordinates = [];
    if (route.geometry?.coordinates) {
      routeCoordinates = route.geometry.coordinates.map((coord) =>
        typeof coord === "string"
          ? [parseFloat(coord.split(" ")[1]), parseFloat(coord.split(" ")[0])]
          : [coord[1], coord[0]]
      );
    }

    if (routeCoordinates.length === 0) {
      throw new Error("OSRM: Empty geometry");
    }

    return {
      routes: [{
        summary: {
          distance: route.distance,
          duration: route.duration,
        },
        geometry: routeCoordinates,
      }],
    };
  } catch (error) {
    console.error("OSRM error:", error);
    throw error;
  }
}

// OpenRouteService Routing (better directions)
const ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjdkMmVlNDMyMTkyZjQ4YjJiNDFlMTQxYjJiMzk1Y2I5IiwiaCI6Im11cm11cjY0In0=";

export async function getRouteORS(startCoords, endCoords) {
  try {
    const response = await fetch("https://api.openrouteservice.org/v2/directions/driving-car", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": ORS_API_KEY,
      },
      body: JSON.stringify({
        coordinates: [
          [startCoords.lng, startCoords.lat],
          [endCoords.lng, endCoords.lat],
        ],
        instructions: true,
      }),
    });

    if (!response.ok) {
      throw new Error(`ORS error: ${response.status}`);
    }

    const data = await response.json();
    console.log("ORS response:", data);

    if (!data.routes || data.routes.length === 0) {
      throw new Error("ORS: No routes found");
    }

    const route = data.routes[0];
    let routeCoordinates = [];
    if (route.geometry) {
      routeCoordinates = decodePolyline(route.geometry);
    }

    if (routeCoordinates.length === 0) {
      throw new Error("ORS: Empty geometry");
    }

    return {
      routes: [{
        summary: {
          distance: route.summary?.distance || 0,
          duration: route.summary?.duration || 0,
        },
        geometry: routeCoordinates,
      }],
    };
  } catch (error) {
    console.error("ORS error:", error);
    throw error;
  }
}

// Main getRoute — tries OSRM first, falls back to ORS
export async function getRoute(startCoords, endCoords) {
  try {
    return await getRouteOSRM(startCoords, endCoords);
  } catch (error) {
    console.warn("OSRM failed, trying ORS:", error.message);
    try {
      return await getRouteORS(startCoords, endCoords);
    } catch (orsError) {
      throw new Error(`Routing failed: OSRM - ${error.message}, ORS - ${orsError.message}`);
    }
  }
}

