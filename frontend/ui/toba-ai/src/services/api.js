import axios from "axios";

export const sendMessage = async (message, lat, lng) => {
  const res = await axios.post("http://127.0.0.1:8000/chat", {
    message,
    lat,
    lng
  });

  return res.data;
};