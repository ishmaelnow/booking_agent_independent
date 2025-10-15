// src/api/booking.js
import axios from "axios";

// Read from env; fallback to same-origin (useful if frontend is served by the API)
const BASE = process.env.REACT_APP_API_URL || "";

const api = axios.create({
  baseURL: BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

/**
 * Post to /book/ride and remap the flat backend response into:
 * { data: { booking: { ... } } }
 * so your existing BookRide.js can keep using response.data.booking.*
 */
export const bookRide = async (payload) => {
  const res = await api.post("/book/ride", payload);
  const r = res.data || {};

  // Remap to the shape BookRide.js is already using
  const booking = {
    // echo inputs so UI can show them without another fetch
    pickup_location: payload.pickup_location,
    dropoff_location: payload.dropoff_location,

    // values returned by backend
    estimated_miles: r.estimated_miles ?? null,
    fare_estimate: r.fare_estimate ?? null,
    fare_explanation: r.fare_explanation ?? "",
    pin: r.pin ?? "",

    // you can add more if you decide to show them later:
    // job_id: r.job_id,
    // dispatch_info: r.dispatch_info,
    // driver_name: r.driver_name,
    // vehicle: r.vehicle,
    // plate: r.plate,
    // eta_minutes: r.eta_minutes,
  };

  // Return in a way that matches your current component usage:
  // setBookingResult(response.data) and then response.data.booking...
  return { data: { booking } };
};

export default api;
