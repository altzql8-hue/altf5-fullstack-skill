# Design system playbook

Create design tokens before composing a complex UI.

## Foundations

- **Typography:** one readable body typeface, 1–2 heading weights, consistent line-height.
- **Color:** semantic tokens (`--surface`, `--text`, `--muted`, `--accent`, `--danger`) with adequate contrast; do not encode status only in color.
- **Spacing:** use a documented spacing scale instead of arbitrary pixel numbers throughout.
- **Elevation:** keep shadow levels sparse, distinguish surfaces by spacing/border rather than excessive blur.
- **Responsive:** design card grids and navigation for touch first; use `minmax`, `clamp` and fluid widths.
- **States:** define default, hover, focus, disabled, loading, error and success for reusable controls.

## Component contract

Specify purpose, props, keyboard behavior, accessibility, error behavior, responsive layout and test scenarios. Never introduce a component solely to hide three lines of HTML. Use screenshots or real UI tests where available rather than claiming visual perfection from static code.
