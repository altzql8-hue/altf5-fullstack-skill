# Engineering recipes

## 1. Responsive dashboard

1. Design content hierarchy and keyboard paths before animation.
2. Start with `templates/frontend`, replace the cards with real user data, and add loading/error/empty states.
3. Add a tested API client rather than hardcoding success responses.
4. Review `references/frontend.md` and `references/design-system.md`.

## 2. Real-time 3D configurator

1. Start with `templates/threejs`; define a mobile frame-time and asset budget.
2. Import assets with an explicit manifest; lazy-load optional geometry and textures.
3. Handle WebGL failures gracefully and dispose resources when changing scenes.
4. Profile on the target device, then read `references/threejs.md`.

## 3. Public API

1. Start with `templates/backend`; identify all trust boundaries and permissions.
2. Use schema validation for every mutation, environment-configured CORS, and per-route authorization where required.
3. Add integration tests for invalid input and expected errors.
4. Follow `references/backend.md`, `references/database.md`, and `references/security.md`.

## 4. Full-stack vertical slice

Implement one end-to-end feature at a time: real HTTP contract → backend validation and test → UI fetch/state management → error handling → deployed smoke test. Avoid building unrelated screens or large abstractions first.
