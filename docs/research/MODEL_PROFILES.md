# Evidence-based coding-agent model profiles (reviewed 2026-11-23)

This file does **not** rank every model in every environment or claim to characterize newest releases. These are diagnostics from one 2026 JetBrains Junie comparison using a particular scaffold and task selection. Model behavior depends on prompts, tools, version, task, harness and evaluation methodology. LLM-judge findings are fallible and a reference patch is not always the only correct fix.

## Observed profiles (not model guarantees)

| Evaluated model | Observations in study | Skill adaptation |
| --- | --- | --- |
| Claude Opus 4.7 | Strong diagnosis and focused patches, but sometimes stopped before complete implementation or skipped executable validation | Require explicit completion checklist, companion call-site search and executable targeted test |
| Gemini 3.5 Flash | Tested often, but sometimes repeated searches, used unverified paths/dependencies and touched unrelated files | Tight search budget, symbol provenance ledger, diff scope verification, stop rule |
| GPT-5.5 | Highest resolution on common subset and consistently checked execution, but assessed hallucinated/redundant changes still occurred | Keep test discipline but verify all claimed APIs, enforce minimal patch/diff quality |
| Qwen 3.6 27B FP8 | Low cost but weaker root-cause diagnosis on comparison tasks | Use on bounded deterministic tasks; escalate ambiguous root-cause reasoning rather than repeatedly retrying |

The study reports 522 common cases for its four-model comparison, with GPT-5.5 resolving 51.5% and Qwen 3.6 27B FP8 resolving 38.9%. It attributes 33.7% of GPT-5.5 and 24.7% of Opus runs as moderate/severe hallucinations in its automated evaluations. Treat these numbers only as results for that setup; do **not** extrapolate to arbitrary code or newer models.

## Adaptation for models not tested in the study

No lab-independent, model-specific flaw list can be responsibly assigned to GPT-6, future Claude, future Gemini, or new open-weight models using those historical numbers. Run representative *local* task evals and compare (1) correct runtime outcome, (2) unverified symbol claims, (3) review burden, (4) extra file changes, (5) time/cost, (6) failure recovery. Switch strategy based on observed failure, not brand folklore.

**Source:** [JetBrains, *From Leaderboards to Model Profiles*, August 2026](https://blog.jetbrains.com/junie/2026/08/from-leaderboards-to-profiles/).
