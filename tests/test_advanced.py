"""Failure-case tests ensure the gates detect the errors they claim to detect."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.route_task import plan_task
from scripts.check_claims import check_claims, confined
from scripts.check_diff_scope import inspect_scope
from scripts.grade_trace import grade
from scripts.security_gate import scan
from scripts.verify_workflows import verify

ROOT = Path(__file__).resolve().parent.parent


class RoutingTests(unittest.TestCase):
    def test_small_task_stays_single_agent(self):
        result = plan_task("Fix CSS padding on the frontend")
        self.assertEqual(result.mode, "single-agent")
        self.assertEqual(result.subagents, [])

    def test_multidomain_security_has_bounded_review(self):
        result = plan_task("Secure frontend authentication and backend API with database access")
        self.assertLessEqual(len(result.subagents), 2)
        self.assertIn("security-reviewer", result.subagents)
        self.assertTrue(result.requires_human_review)

    def test_subagents_can_be_disabled(self):
        result = plan_task("frontend and backend", max_subagents=0)
        self.assertEqual(result.subagents, [])

    def test_invalid_empty(self):
        with self.assertRaises(ValueError):
            plan_task(" ")


class EvidenceTests(unittest.TestCase):
    def test_claims_pass_and_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "package.json").write_text('{"dependencies":{"zod":"^4"}}')
            (root / "testlog.json").write_text('{"command":"npm test","exit_code":0}')
            claims = [
                {"id":"file", "type":"file_exists", "path":"package.json"},
                {"id":"package", "type":"package_declared", "path":"package.json", "package":"zod"},
                {"id":"log", "type":"command_passed", "log":"testlog.json", "command":"npm test"},
                {"id":"fake", "type":"contains_text", "path":"package.json", "text":"not-there"},
                {"id":"no", "type":"package_declared", "path":"package.json", "package":"invented-lib"},
            ]
            results = check_claims(root, claims)
            self.assertEqual([x["pass"] for x in results], [True, True, True, False, False])

    def test_rejects_directory_escape(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaises(ValueError):
                confined(root, "../secret.txt")
            self.assertFalse(check_claims(root, [{"type":"file_exists", "path":"../secret.txt"}])[0]["pass"])

    def test_lying_exit_code_not_truthy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "log.json").write_text('{"command":"npm test","exit_code":false}')
            results = check_claims(root, [{"type":"command_passed", "log":"log.json", "command":"npm test"}])
            self.assertFalse(results[0]["pass"])


class ScopeTests(unittest.TestCase):
    def test_out_of_scope_blocked(self):
        result = inspect_scope(["src/view.ts", "LICENSE"], ["src/**"], ["LICENSE"])
        self.assertTrue(any("LICENSE" in line for line in result))

    def test_protected_allowed_path_blocked(self):
        result = inspect_scope([".github/workflows/ci.yml"], [".github/**"], [".github/**"])
        self.assertTrue(result)


class TraceTests(unittest.TestCase):
    def test_fake_success_without_checks_fails(self):
        self.assertFalse(grade({"claims": [{"verified": True}], "checks": []})["pass"])

    def test_hallucination_or_budget_fails(self):
        result = grade({"claims": [{"verified": False}], "checks": [{"passed": True}],
                        "tools": [{"name": "cat", "signature": "cat a"}] * 4}, max_tools=3)
        self.assertFalse(result["pass"])
        self.assertEqual(result["duplicate_tool_signatures"], 3)

    def test_verified_case_passes(self):
        self.assertTrue(grade({"claims": [{"verified": True}], "checks": [{"passed": True}],
                               "tools": [], "subagents": []})["pass"])


class SecurityTests(unittest.TestCase):
    def test_sensitive_file_and_insecure_code(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".env").write_text("EXAMPLE=placeholder")
            (root / "code.js").write_text('process.env.NODE_TLS_REJECT_UNAUTHORIZED="0";\n')
            rules = {x.rule for x in scan(root)}
            self.assertIn("sensitive-file", rules)
            self.assertIn("disabled-tls-verification", rules)

    def test_starters_do_not_trigger_heuristics(self):
        for name in ("frontend", "threejs", "backend"):
            with self.subTest(name=name):
                self.assertEqual(scan(ROOT / "templates" / name), [])

    def test_workflows_pinned_and_least_privilege(self):
        self.assertEqual(verify(ROOT / ".github" / "workflows"), [])

    def test_unpinned_workflow_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "bad.yml").write_text('permissions:\n  contents: read\njobs:\n  test:\n    timeout-minutes: 10\n    steps:\n      - uses: actions/checkout@v4\n')
            self.assertTrue(any("not pinned" in error for error in verify(path)))


if __name__ == "__main__":
    unittest.main()
