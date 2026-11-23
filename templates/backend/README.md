# Express backend starter

Express 5 + Zod + TypeScript. A functional example API with `GET /health`, `GET /api/notes`, and `POST /api/notes` (body `{ "message": "hello" }`). Stores notes **in memory only**; migrate to a production database before deployment. Includes request limits, predictable error JSON, strict validation, security headers and an exact-origin CORS allowlist.

```sh
npm install
npm run typecheck
npm run build
npm test
npm run dev
```

Configure `PORT` and `CORS_ORIGIN` via environment variables (see `.env.example`). Do not commit real `.env` files. This is a demo API, not a production auth/rate-limiting solution.
