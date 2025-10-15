// src/api/jobs.js
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL || "";

const api = axios.create({
  baseURL: BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

// GET /jobs/view
export const viewJobs = () => api.get("/jobs/view");

// POST /jobs/claim?job_id=...&driver_name=...
export const claimJob = (job_id, driver_name) =>
  api.post("/jobs/claim", null, {
    params: { job_id, driver_name },
  });

// POST /complete/ride?job_id=...&driver_name=...
export const completeJob = (job_id, driver_name) =>
  api.post("/complete/ride", null, {
    params: { job_id, driver_name },
  });

export default api;