const dev = process.env.NODE_ENV !== "production";

export const API_BASE_URL = dev
  ? "http://localhost:8000"
  : "";