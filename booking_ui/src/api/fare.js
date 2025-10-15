// src/api/fare.js
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL || "";

const api = axios.create({
  baseURL: BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

export const getFareEstimate = async (miles, options = {}) => {
  const params = { miles, ...options };
  return await api.get("/fare/preview", { params });
};

export default api;