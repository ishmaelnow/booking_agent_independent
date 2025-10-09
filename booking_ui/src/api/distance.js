import axios from "axios";

export const fetchDistance = (pin) =>
  axios.post("http://localhost:8000/distance", { pin });