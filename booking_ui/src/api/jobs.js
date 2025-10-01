import axios from "axios";
export const viewJobs = () => axios.get("http://localhost:8000/jobs/view");
export const claimJob = (job_id, driver_name) =>
  axios.post(`http://localhost:8000/jobs/claim?job_id=${job_id}&driver_name=${driver_name}`);
export const completeJob = (job_id, driver_name) =>
  axios.post(`http://localhost:8000/complete/ride?job_id=${job_id}&driver_name=${driver_name}`);