# Contributing to AltF5 Fullstack Engineering

Thank you for helping make agent-written software more reliable.

1. Fork the project and work from a feature branch.
2. Keep `SKILL.md` short and put detailed topic guidance in `references/`.
3. Add an automated test when changing validators or scaffolding.
4. Validate examples using `npm install`, `npm run typecheck`, and `npm run build` in the affected template.
5. Run `python scripts/validate_skill.py` and `python -m unittest discover -s tests -v`.
6. Open a pull request describing behavior, evidence, backwards compatibility, and screenshots for UI changes.

Respect third-party licenses. Never commit secrets, API keys, proprietary game files, datasets without redistribution rights, or personal data. Be respectful and specific in reviews.
