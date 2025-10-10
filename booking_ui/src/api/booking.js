import { api } from "./client";

export const bookRide = (data) => api.post("/book/ride", data);