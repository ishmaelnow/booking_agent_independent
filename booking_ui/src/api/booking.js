import axios from "axios";
export const bookRide = (data) =>
  axios.post("http://localhost:8000/book/ride", data);