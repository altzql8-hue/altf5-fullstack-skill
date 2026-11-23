# Performance engineering playbook

## Measure first

- Define target hardware, network, page type, traffic and expected concurrency.
- Record baseline p75 Core Web Vitals (LCP, INP, CLS), memory footprint and API p95 latency.
- For Three.js record `renderer.info`, CPU and GPU frame time, draw calls, triangles and texture allocations on actual mobile hardware.

## Frontend

- Route-level code splitting; lazy-load optional 3D views; size and compress media appropriately.
- Use modern image formats and dimensions; avoid content layout shifts.
- Avoid deeply nested effects, repeated network queries and unnecessary component rerenders.
- Provide cache headers and invalidation plans; don't cache sensitive API responses publicly.

## Backend

- Index high-cardinality filters, profile slow queries, cap pagination, pool connections carefully.
- Bound concurrency/queue growth and define timeout and retry policies; avoid retry storms.
- Observe p95/p99 latency, CPU, RSS, error rate, request rate and external-service timing.

## Budget tool

`python scripts/check_performance.py path/to/dist --max-total-kib 4096 --max-file-kib 1024`

This measures **uncompressed artifact sizes** and fails when thresholds are exceeded. It does not measure runtime FPS, API latency or real-world network load. Track gzipped/brotli budgets separately if required.
