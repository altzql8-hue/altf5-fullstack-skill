"""Regression tests for local, zero-dependency skill tools."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_code import audit
from scripts.check_performance import measure
from scripts.scaffold import available, scaffold
from scripts.validate_project import validate as validate_project
from scripts.validate_skill import parse_frontmatter, validate as validate_skill

ROOT = Path(__file__).resolve().parent.parent


class SkillValidationTests(unittest.TestCase):
    def test_repo_skill_valid(self):
        self.assertEqual(validate_skill(ROOT, check_directory_name=False), [])

    def test_missing_frontmatter_rejected(self):
        with self.assertRaises(ValueError):
            parse_frontmatter("# not metadata")

    def test_mismatched_name_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "wrong-folder"
            folder.mkdir()
            (folder / "SKILL.md").write_text("---\nname: actual-name\ndescription: test\nlicense: MIT\n---\n")
            (folder / "LICENSE").write_text("MIT")
            self.assertTrue(any("match parent" in x for x in validate_skill(folder)))

    def test_broken_markdown_links_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "good-name"
            folder.mkdir()
            (folder / "SKILL.md").write_text("---\nname: good-name\ndescription: test\nlicense: MIT\n---\n[broken](missing.md)\n")
            (folder / "LICENSE").write_text("MIT")
            self.assertTrue(any("broken local link" in x for x in validate_skill(folder)))


class StarterTests(unittest.TestCase):
    def test_all_starters_valid(self):
        self.assertEqual(set(available()), {"frontend", "threejs", "backend"})
        for template in available():
            with self.subTest(template=template):
                self.assertEqual(validate_project(ROOT / "templates" / template), [])

    def test_scaffold_copy_and_rename(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "my-project"
            scaffold("frontend", folder)
            self.assertEqual(json.loads((folder / "package.json").read_text())["name"], "my-project")
            self.assertTrue((folder / "src" / "App.tsx").exists())
            with self.assertRaises(FileExistsError):
                scaffold("frontend", folder)

    def test_unknown_starter(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                scaffold("unknown", Path(temp) / "nope")

    def test_invalid_project_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(validate_project(Path(temp)))


class SafetyAndBudgetTests(unittest.TestCase):
    def test_audit_finds_eval_and_env(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "demo.ts").write_text("const x = eval(input);\n")
            (folder / ".env").write_text("DO_NOT_COMMIT=true\n")
            rules = {f.rule for f in audit(folder)}
            self.assertIn("dynamic-eval", rules)
            self.assertIn("committed-env-file", rules)

    def test_clean_starters_audit(self):
        for template in available():
            with self.subTest(template=template):
                self.assertEqual(audit(ROOT / "templates" / template), [])

    def test_budget_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "a.js").write_bytes(b"x" * 2048)
            errors, total, count = measure(folder, max_total_kib=1, max_file_kib=1)
            self.assertEqual((total, count), (2048, 1))
            self.assertEqual(len(errors), 2)

    def test_empty_build_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            errors, _, count = measure(Path(temp))
            self.assertEqual(count, 0)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
