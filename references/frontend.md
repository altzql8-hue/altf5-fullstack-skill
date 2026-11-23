# Frontend engineering playbook

## Architecture

- Prefer TypeScript strict mode, feature-owned components, small state boundaries, and a single source of truth for fetched data.
- Pick a framework only after identifying rendering requirements (SPA vs SSR vs static). Do not install Next.js for a trivial static page.
- Separate server data, ephemeral view state, and persisted preferences; avoid storing derived values.
- Use reusable components where repeated behavior exists, not for every HTML tag.

## Accessibility and interaction

- Prefer semantic HTML (`button`, `nav`, `main`, `form`, proper headings) to div-click handlers.
- Ensure every input has a visible label; show focus indicators; keyboard navigation should reach every active control.
- Supply `aria-live` for asynchronous result announcements; avoid redundant aria on native elements.
- Meet WCAG 2.2 AA where applicable; test 200% zoom, narrow screens, and reduced-motion setting.
- Include actual loading, error, zero-results, and success states. Disable actions only when required; explain failures in text.

## Visual quality

- Define a compact token scale for colors, spacing, radius, shadow and typography in CSS custom properties.
- Use responsive layouts with content-led breakpoints; avoid horizontal page scroll.
- Use purposeful motion below ~200–300 ms for frequent transitions and switch off nonessential motion with `prefers-reduced-motion`.
- Avoid generic loading spinners as sole state indication; show meaningful skeletons or status messages.

## Verification

1. Build and run; inspect console/network errors.
2. Test mouse, touch, keyboard, and 360px width.
3. Confirm form behavior, malformed input, network errors, loading and empty states.
4. Check headings, labels, focus, and accessible names.
5. Capture real performance traces before changing architecture.

Starter: [`templates/frontend`](../templates/frontend/README.md).
