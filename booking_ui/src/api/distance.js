import { api } from "./client";

export const fetchDistance = (pin) => {
  return api.post("/distance", { pin });
};