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