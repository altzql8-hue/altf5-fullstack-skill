# Research notebook — reviewed 2026-11-23

Use these primary engineering references and cite the study scope when repeating numerical claims. Do not assert that a framework, model, security standard or leaderboard has remained unchanged after this review date.

1. [JetBrains — From Leaderboards to Model Profiles (August 2026)](https://blog.jetbrains.com/junie/2026/08/from-leaderboards-to-profiles/). Harness-dependent observations about GPT-5.5, Opus 4.7, Gemini 3.5 Flash and Qwen 3.6; never generalize across all deployments.
2. [OpenAI — Separating signal from noise in coding evaluations (July 2026)](https://openai.com/index/separating-signal-from-noise-coding-evaluations/). Documents low coverage, underspecification and implementation-specific grading errors; do not treat benchmark pass as complete correctness.
3. [Anthropic — Building effective agents (2024)](https://www.anthropic.com/research/building-effective-agents). Minimum necessary architecture; orchestration patterns; prefer simple workflows when sufficient.
4. [Anthropic — How we built our multi-agent research system (June 2025)](https://www.anthropic.com/research/multi-agent-research-system). Multi-agent benefits in parallel research and substantial token/cost overhead; tightly coupled coding is less parallelizable.
5. [Anthropic — Effective context engineering for AI agents (2025)](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). Efficient context and bounded specialist roles.
6. [Anthropic — Demystifying evals for AI agents (2026)](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Positive/negative eval design and transcript grading.
7. [GitHub — Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use). SHA pinning, least-privilege tokens and workflow injection risks.
8. [GitHub — About Dependabot](https://docs.github.com/en/code-security/concepts/supply-chain-security/about-the-dependabot-yml-file). Dependency update configuration.
9. [OWASP — Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) and [ASVS 5.0](https://asvs.owasp.org/). Defensive application-security guidance.
10. [OpenAI — Practical approach to verifying code at scale](https://openai.com/safety-alignment/scaling-code-verification/). High-signal, evidence-backed code review tradeoffs.

## Research limits

- Findings may describe agents/harnesses, not intrinsic model traits.
- Agent traces can be incomplete and model judges can be wrong.
- Default scripts are stdlib heuristics, not evaluation of a live model or exploit-proof analysis.
- Real superiority claims require controlled repeated runs of comparable tasks, with baseline, costs and manual outcome verification.

11. [SecureAgentBench (September 2025)](https://arxiv.org/abs/2509.22097). Functionality is not sufficient for security; prompt-only safeguards have limitations.
12. [Last Secure Code Benchmark (October 2026)](https://arxiv.org/abs/2610.14766). Model/harness-dependent correct-and-secure evaluation.
13. [Task-grounded reasoning failures (October 2026)](https://arxiv.org/abs/2610.32338). Concrete agent claims can be incorrect even with a plausible workflow.
14. [Survey of coding agent security (2026)](https://www.sciencedirect.com/science/article/pii/S0950584926002776). Tool/repository-content attacks and evidence gaps.
15. [OWASP GitHub Actions Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html). Workflow injection, credential boundaries and SHA pinning.
16. [V3 failure-to-control mapping](V3_FINDINGS.md). What V3 changes and what it cannot verify.
