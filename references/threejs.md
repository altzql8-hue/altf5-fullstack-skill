# Three.js / WebGL engineering playbook

## Initial design

- Confirm whether the output is a real-time WebGL application, an offline render, a glTF viewer, or a generated video.
- Use ES modules and a bundler (Vite) for applications; keep Three.js and addons on the same version.
- Start with WebGL renderer compatibility. WebGPU is promising, but do not assume every Android device/browser supports it.
- Decide on a polygon/texture/draw-call budget for target phone hardware; test using real devices.

## Essential lifecycle

1. Initialize scene, camera, renderer and event handlers only once per mount.
2. Handle resizing using parent bounds and device pixel ratio cap, e.g. `Math.min(devicePixelRatio, 2)`.
3. Drive animation using `renderer.setAnimationLoop` or requestAnimationFrame and delta time; avoid frame-dependent motion.
4. On unmount, stop the loop, unregister events/observers, dispose geometry/materials/textures, and remove the canvas.
5. Detect missing WebGL and show an accessible message; handle context-lost and restored scenarios where possible.

## Rendering costs

- Prefer instanced meshes for repeated objects, LOD for distant assets, and frustum culling where useful.
- Compress textures and avoid defaulting everything to 4K; manage GPU memory and pixel ratio.
- Use fewer shadow-casting lights, fixed-cost postprocessing, and a deliberately bounded reflection strategy.
- Measure draw calls, geometry counts, textures and total GPU memory. `renderer.info` is informative, not a hardware profiler.
- Profile shader compilation spikes and asset-load pauses; avoid blocking first meaningful paint.

## Input and accessibility

- Normalize touch/mouse coordinates against canvas bounds; use pointer events where practical.
- Ensure gamepad/touch actions are discoverable; provide a non-3D fallback or summary for key content.
- Respect reduced motion; pause/reduce animation when the page is hidden or not visible.

## Verification

- Test WebGL unavailable, canvas resize, browser tab hidden, mobile touch, high-DPI devices, disposal and route changes.
- Profile target GPU frame times; 16.7ms is the nominal frame budget for 60 FPS, not a promise.

Starter: [`templates/threejs`](../templates/threejs/README.md). Documentation: https://threejs.org/docs/ and https://threejs.org/manual/.
