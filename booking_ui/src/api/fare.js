// src/api/fare.js
import { api } from "./client";

export const getFareEstimate = (miles) => {
  return api.get(`/fare/estimate?miles=${miles}`);
};