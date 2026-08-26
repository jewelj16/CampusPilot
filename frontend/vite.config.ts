import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Proxies /api to the FastAPI backend during local dev so the frontend
// never needs to know the backend's host/port, and CORS is a non-issue
// in dev regardless of what CORS_ORIGINS is set to on the backend.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: process.env.VITE_API_PROXY_TARGET ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
