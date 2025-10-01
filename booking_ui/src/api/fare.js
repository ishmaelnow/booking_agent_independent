import axios from "axios";
export const getFareEstimate = (miles) =>
  axios.get(`http://localhost:8000/fare/estimate?miles=${miles}`);