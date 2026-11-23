#!/usr/bin/env python3
"""Compare matched before/after agent eval traces, never just self-reported scores.

Input: {"tasks":[{"id":"fixed-001","passed":true,"tokens":1000,"tool_calls":20}]}
Keep the task, tests, runner and measurement source identical between runs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def index(data: dict) -> dict:
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("tasks must be a nonempty list")
    result = {}
    for item in tasks:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            raise ValueError("each task needs a nonempty id")
        if item["id"] in result:
            raise ValueError(f"duplicate task id: {item['id']}")
        if type(item.get("passed")) is not bool:
            raise ValueError(f"task {item['id']}: passed must be a boolean")
        for metric in ("tokens", "tool_calls"):
            value = item.get(metric)
            if value is not None and (type(value) is not int or value < 0):
                raise ValueError(f"task {item['id']}: {metric} must be nonnegative integer")
        result[item["id"]] = item
    return result


def compare(baseline: dict, candidate: dict) -> dict:
    before, after = index(baseline), index(candidate)
    if before.keys() != after.keys():
        raise ValueError("task sets must match exactly; cannot hide missing/failed tasks")
    ids = sorted(before)
    regressed = [i for i in ids if before[i]["passed"] and not after[i]["passed"]]
    improved = [i for i in ids if not before[i]["passed"] and after[i]["passed"]]
    comparable = {}
    for metric in ("tokens", "tool_calls"):
        matched = [(before[i][metric], after[i][metric]) for i in ids
                   if before[i].get(metric) is not None and after[i].get(metric) is not None]
        comparable[metric] = None if not matched else {
            "paired_tasks": len(matched), "baseline_total": sum(a for a, b in matched),
            "candidate_total": sum(b for a, b in matched),
            "saved": sum(a - b for a, b in matched),
            "relative_savings_percent": None if sum(a for a, b in matched) == 0 else
                round(100 * sum(a - b for a, b in matched) / sum(a for a, b in matched), 2),
        }
    return {"tasks": len(ids), "baseline_passed": sum(before[i]["passed"] for i in ids),
            "candidate_passed": sum(after[i]["passed"] for i in ids), "regressed": regressed,
            "improved": improved, "usage": comparable, "no_quality_regression": not regressed,
            "warning": "Only meaningful for identical task sets, held-out tests, environment and trusted telemetry."}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("baseline", type=Path)
    p.add_argument("candidate", type=Path)
    p.add_argument("--fail-on-regression", action="store_true")
    args = p.parse_args()
    try:
        report = compare(json.loads(args.baseline.read_text()), json.loads(args.candidate.read_text()))
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    print(json.dumps(report, indent=2))
    return int(args.fail_on_regression and not report["no_quality_regression"])


if __name__ == "__main__":
    raise SystemExit(main())
