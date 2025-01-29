import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || `http://localhost:${process.env.BACKEND_PORT}/api`,
});

export default api;