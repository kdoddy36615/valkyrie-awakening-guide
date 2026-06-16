import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The app lives in app/ but imports data/*.json and sources/ images from the
// repo root, so the dev server must be allowed to serve the whole repo.
export default defineConfig({
  plugins: [react()],
  root: "app",
  publicDir: false,
  server: {
    fs: { allow: [".."] },
  },
  build: {
    outDir: "../dist",
    emptyOutDir: true,
  },
});
