# Single-process local runtime

The app runs as one process: FastAPI serves the REST API and the built SPA static assets on a single port (default localhost). One command starts the Instance; no separate frontend server in production.

Development uses a split setup (Vite dev server + API) for hot reload. A desktop wrapper (Tauri, pywebview) was considered but deferred — browser to localhost is sufficient for v1.

**Considered options:** Single process (chosen), separate dev/prod servers only, desktop wrapper from day one.

**Consequences:** Deployment is a Python package or script plus a built frontend bundle. Each family device runs its own Instance independently.
