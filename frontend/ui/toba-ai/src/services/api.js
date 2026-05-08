const API_URL = "http://127.0.0.1:8000";


export async function sendMessage(
  message,
  destinationPayload = null,
  mobileData = null
) {

  try {

    const response = await fetch(
      `${API_URL}/chat`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message,
          destinationPayload,
          mobileData,
          user_id: "default_user",
        }),
      }
    );

    if (!response.ok) {

      throw new Error(
        "Request gagal"
      );
    }

    return await response.json();

  } catch (err) {

    console.error(
      "API ERROR:",
      err
    );

    return {
      intent: "error",

      reply:
        "Backend tidak dapat dihubungkan.",

      data: {},
    };
  }
}


/* ========================================
   GPS
======================================== */

export async function saveUserLocation(
  lat,
  lng
) {

  console.log(
    "GPS LOCATION:",
    lat,
    lng
  );

  return {
    success: true,
  };
}


/* ========================================
   ROUTE MOCK
======================================== */

export async function getRoute(
  startCoords,
  endCoords
) {

  return {
    routes: [
      {
        summary: {
          distance: 120000,
          duration: 14400,
        },

        geometry: [
          [
            startCoords.lng,
            startCoords.lat,
          ],

          [
            endCoords.lng,
            endCoords.lat,
          ],
        ],
      },
    ],
  };
}