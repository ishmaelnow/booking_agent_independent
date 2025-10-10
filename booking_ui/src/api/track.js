// src/api/track.js
import { api } from "./client";

export const fetchLiveLocations = (pin) => {
  return api.get(`/track/live?pin=${pin}`);
};