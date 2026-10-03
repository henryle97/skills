"""Regression tests run against temporary repositories, never user skill folders."""

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RepoToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.home = self.root / "home"
        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
        shutil.copytree(ROOT / "template", self.repo / "template")
        (self.repo / "skills").mkdir()
        self.home.mkdir()
        validator.errors.clear()
        validator.warnings.clear()

    def run_script(self, name, *args):
        return subprocess.run(
            ["bash", str(self.repo / "scripts" / name), *args],
            env={**os.environ, "HOME": str(self.home)},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_scaffolding_rejects_unknown_or_extra_arguments(self):
        for args in [(), ("demo", "--user-invokedd"), ("demo", "--user-invoked", "extra")]:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_script("new-skill.sh", *args).returncode, 0)
                self.assertFalse((self.repo / "skills/demo").exists())

    def test_scaffolding_invocation_modes(self):
        for name, flags in [("implicit", []), ("explicit", ["--user-invoked"])]:
            with self.subTest(name=name):
                result = self.run_script("new-skill.sh", name, *flags)
                self.assertEqual(result.returncode, 0, result.stderr)
                validator.check_openai_yaml(self.repo / "skills" / name, name, bool(flags))
                self.assertEqual(validator.errors, [])

    def test_linking_preserves_foreign_paths(self):
        self.assertEqual(self.run_script("new-skill.sh", "demo").returncode, 0)
        for kind in ["directory", "live-link", "broken-link"]:
            with self.subTest(kind=kind):
                destination = self.home / ".agents/skills"
                destination.mkdir(parents=True, exist_ok=True)
                target = destination / "demo"
                foreign = self.root / kind
                if kind == "directory":
                    target.mkdir()
                else:
                    if kind == "live-link":
                        foreign.mkdir()
                    target.symlink_to(foreign)
                result = self.run_script("link-skills.sh")
                self.assertEqual(result.returncode, 0, result.stderr)
                if kind == "directory":
                    self.assertFalse(target.is_symlink())
                    target.rmdir()
                else:
                    self.assertEqual(target.readlink(), foreign)
                    target.unlink()

    def test_owned_links_are_idempotent_and_unlinked(self):
        self.assertEqual(self.run_script("new-skill.sh", "demo").returncode, 0)
        for _ in range(2):
            result = self.run_script("link-skills.sh")
            self.assertEqual(result.returncode, 0, result.stderr)
        for folder in [".agents/skills", ".claude/skills"]:
            self.assertEqual((self.home / folder / "demo").resolve(), self.repo / "skills/demo")
        self.assertEqual(self.run_script("link-skills.sh", "--unlink").returncode, 0)
        self.assertFalse((self.home / ".agents/skills/demo").is_symlink())
        self.assertFalse((self.home / ".claude/skills/demo").is_symlink())

    def test_versions_must_increase_numerically(self):
        for version, base, accepted in [
            ("0.1.1", "0.1.0", True),
            ("0.10.0", "0.9.9", True),
            ("1.0.0", "0.99.99", True),
            ("0.1.0", "0.1.0", False),
            ("0.0.9", "0.1.0", False),
            ("0.9.0", "0.10.0", False),
            ("invalid", "0.1.0", False),
            ("01.0.0", "0.1.0", False),
            ("1.0.0", "invalid", False),
        ]:
            with self.subTest(version=version, base=base):
                result = self.run_script("check-version.sh", version, base)
                self.assertEqual(result.returncode == 0, accepted, result.stderr)

    def test_openai_yaml_reports_invalid_shapes(self):
        skill = self.repo / "skills/demo"
        (skill / "agents").mkdir(parents=True)
        for content, expected in [
            ("- item\n", "must be a YAML mapping"),
            ("scalar\n", "must be a YAML mapping"),
            ("", "must be a YAML mapping"),
            ("interface: [item]\n", "interface must be a YAML mapping"),
            ("interface: null\n", "interface must be a YAML mapping"),
            ("policy: [item]\n", "policy must be a YAML mapping"),
            ("policy: null\n", "policy must be a YAML mapping"),
            ('policy:\n  allow_implicit_invocation: "false"\n', "must be a boolean"),
        ]:
            with self.subTest(content=content):
                validator.errors.clear()
                (skill / "agents/openai.yaml").write_text(content)
                validator.check_openai_yaml(skill, "demo", False)
                self.assertTrue(any(expected in error for error in validator.errors))


if __name__ == "__main__":
    unittest.main()
