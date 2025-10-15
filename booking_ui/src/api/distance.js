// src/api/distance.js
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL;

export function fetchDistance(pin) {
  // Backend expects { pin: number }
  return axios.post(`${BASE}/distance`, { pin });
}
