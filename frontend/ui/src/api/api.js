import axios from "axios";

const BASE = "http://localhost:8000";

export const sendChat = async (message) => {
  const res = await axios.post(`${BASE}/chat`, {
    message,
  });
  return res.data;
};

export const fetchSimulation = async () => {
  const res = await axios.get(`${BASE}/simulate`);
  return res.data;
};