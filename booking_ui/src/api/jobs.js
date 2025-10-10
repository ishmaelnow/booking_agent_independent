import { api } from "./client";

export const viewJobs = () => api.get("/jobs/view");
export const claimJob = (job_id, driver_name) =>
  api.post(`/jobs/claim?job_id=${job_id}&driver_name=${driver_name}`);
export const completeJob = (job_id, driver_name) =>
  api.post(`/complete/ride?job_id=${job_id}&driver_name=${driver_name}`);