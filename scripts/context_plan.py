#!/usr/bin/env python3
"""Deterministically prioritize *paths* for a task within an approximate context budget.

No file contents leave this tool, and its ranking is advisory, not a semantic oracle.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IGNORE = {".git", "node_modules", "dist", "coverage", ".next", ".artifacts", "__pycache__", ".venv"}
BLOCKED = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".json", ".toml", ".yml", ".yaml", ".css", ".html"}
DOMAINS = {
    "threejs": {"three", "webgl", "webgpu", "shader", "gpu", "scene", "3d"},
    "frontend": {"react", "frontend", "css", "ui", "ux", "component", "accessibility"},
    "backend": {"express", "backend", "server", "api", "endpoint"},
    "database": {"postgres", "database", "sql", "migration", "firebase"},
    "security": {"security", "auth", "secret", "permission", "vulnerability"},
}


def plan(root: Path, task: str, budget_tokens: int = 5000) -> dict:
    if budget_tokens < 128:
        raise ValueError("budget_tokens must be >=128")
    words = set(re.findall(r"[a-z0-9]+", task.lower()))
    if not words:
        raise ValueError("task cannot be blank")
    relevant = {d for d, aliases in DOMAINS.items() if words & aliases}
    files = []
    root = root.resolve()
    for file in root.rglob("*"):
        if not file.is_file() or file.is_symlink():
            continue
        relative = file.relative_to(root)
        if any(part in IGNORE or part.startswith(".env") for part in relative.parts):
            continue
        if file.name in BLOCKED or file.suffix not in EXTENSIONS or file.stat().st_size > 1_000_000:
            continue
        path = relative.as_posix()
        tokens = set(re.findall(r"[a-z0-9]+", path.lower()))
        score = len(tokens & words) * 9 + sum(6 for domain in relevant if domain in tokens)
        if file.name in {"SKILL.md", "AGENTS.md", "README.md"}:
            score += 4
        if file.suffix in {".ts", ".tsx", ".py"} and score:
            score += 1
        estimate = max(1, (file.stat().st_size + 3) // 4)
        if score > 0:
            files.append((score, estimate, path))
    files.sort(key=lambda item: (-item[0], item[1], item[2]))
    selected, used = [], 0
    for score, estimate, path in files:
        if used + estimate <= budget_tokens:
            selected.append({"path": path, "relevance": score, "estimated_tokens": estimate})
            used += estimate
    return {"task": task, "budget_tokens": budget_tokens, "estimated_tokens_selected": used,
            "candidate_count": len(files), "selected": selected,
            "note": "Size/4 is a rough estimate; inspect selected files and imports before editing."}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("task")
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--budget-tokens", type=int, default=5000)
    args = p.parse_args()
    try:
        print(json.dumps(plan(args.root, args.task, args.budget_tokens), indent=2))
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
