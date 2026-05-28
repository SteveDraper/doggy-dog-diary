import fs from "node:fs";
import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

function readBackendPort(): number {
  const configPath = path.resolve(__dirname, "../config.yaml");
  if (!fs.existsSync(configPath)) {
    return 8080;
  }
  const match = fs.readFileSync(configPath, "utf8").match(/^port:\s*(\d+)\s*$/m);
  return match ? Number(match[1]) : 8080;
}

const backendPort = readBackendPort();

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: `http://127.0.0.1:${backendPort}`,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: path.resolve(__dirname, "../backend/static/spa"),
    emptyOutDir: true,
  },
});
