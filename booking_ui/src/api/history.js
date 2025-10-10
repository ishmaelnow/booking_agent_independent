// src/api/history.js
import { api } from "./client";

export const fetchRideHistory = (pin) => {
  return api.get("/book/history", {
    params: { pin: String(pin).trim() },
  });
};