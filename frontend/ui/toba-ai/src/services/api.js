import axios from "axios";

export const sendMessage = (msg) => {
  return axios.post("http://127.0.0.1:8000/chat", {
    message: msg
  });
};