#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Validate every skill and plugin manifest in this repo.

Run `scripts/validate.py` (needs uv). Pass `--external` to also run the
harness validators (`claude plugin validate`, Codex's validate_plugin.py) when
they are installed.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKET = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKET = ROOT / ".agents" / "plugins" / "marketplace.json"
CODEX_VALIDATOR = Path.home() / ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
MAX_BODY_LINES = 500

errors: list[str] = []
warnings: list[str] = []


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    data = yaml.safe_load(text[4:end])
    return (data if isinstance(data, dict) else None), text[end + 4 :]


def check_skill(skill_dir: Path) -> int:
    """Validate one skill folder and return its description length."""
    label = f"skills/{skill_dir.name}"
    if skill_dir.is_symlink():
        errors.append(f"{label}: is a symlink; Codex drops symlinks when installing plugins")
        return 0
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{label}: missing SKILL.md")
        return 0

    try:
        fm, body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{label}/SKILL.md: frontmatter is not valid YAML ({exc})")
        return 0
    if fm is None:
        errors.append(f"{label}/SKILL.md: must start with a closed YAML frontmatter block")
        return 0

    name = fm.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(
            f"{label}: name {name!r} must be lowercase a-z0-9 joined by single '-', max 64 chars"
        )
    elif name != skill_dir.name:
        errors.append(f"{label}: name {name!r} must equal the folder name")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{label}: description is required")
        desc = ""
    elif len(desc) > 1024:
        errors.append(f"{label}: description is {len(desc)} chars, max 1024")
    elif "<" in desc or ">" in desc:
        errors.append(f"{label}: description must not contain '<' or '>'")

    compat = fm.get("compatibility")
    if compat is not None and (not isinstance(compat, str) or len(compat) > 500):
        errors.append(f"{label}: compatibility must be a string of at most 500 chars")

    body_lines = body.count("\n")
    if body_lines > MAX_BODY_LINES:
        warnings.append(f"{label}/SKILL.md: body is {body_lines} lines; move detail to references/")

    nested = [p for p in skill_dir.rglob("SKILL.md") if p != skill_md]
    for path in nested:
        errors.append(
            f"{path.relative_to(ROOT)}: nested skills are not allowed; Codex would load it as a separate skill"
        )

    check_openai_yaml(skill_dir, label, fm.get("disable-model-invocation") is True)
    return len(desc)


def check_openai_yaml(skill_dir: Path, label: str, user_invoked: bool) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        errors.append(f"{label}: missing agents/openai.yaml")
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{label}/agents/openai.yaml: not valid YAML ({exc})")
        return

    if not isinstance(data, dict):
        errors.append(f"{label}/agents/openai.yaml: must be a YAML mapping")
        return

    interface = data.get("interface", {})
    if not isinstance(interface, dict):
        errors.append(f"{label}/agents/openai.yaml: interface must be a YAML mapping")
        interface = {}
    for field in ("display_name", "short_description"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"{label}/agents/openai.yaml: interface.{field} is required")
    short = interface.get("short_description")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        warnings.append(
            f"{label}/agents/openai.yaml: short_description is {len(short)} chars, Codex suggests 25 to 64"
        )

    policy = data.get("policy", {})
    if not isinstance(policy, dict):
        errors.append(f"{label}/agents/openai.yaml: policy must be a YAML mapping")
        return
    implicit = policy.get("allow_implicit_invocation", True)
    if not isinstance(implicit, bool):
        errors.append(
            f"{label}/agents/openai.yaml: policy.allow_implicit_invocation must be a boolean"
        )
        return
    if user_invoked and implicit is not False:
        errors.append(
            f"{label}: disable-model-invocation is true but agents/openai.yaml lacks "
            "policy.allow_implicit_invocation: false"
        )
    if not user_invoked and implicit is False:
        errors.append(
            f"{label}: agents/openai.yaml sets allow_implicit_invocation: false but SKILL.md "
            "lacks disable-model-invocation: true"
        )


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


def check_manifests() -> None:
    claude, codex = load_json(CLAUDE_PLUGIN), load_json(CODEX_PLUGIN)
    claude_market, codex_market = load_json(CLAUDE_MARKET), load_json(CODEX_MARKET)

    versions = {"claude": claude.get("version"), "codex": codex.get("version")}
    for tool, version in versions.items():
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            errors.append(f"{tool} plugin.json: version {version!r} must be x.y.z")
    if len(set(versions.values())) > 1:
        errors.append(f"plugin versions differ: {versions}; run scripts/bump-version.sh")

    name = claude.get("name")
    if codex.get("name") != name:
        errors.append(f"plugin names differ: claude={name!r} codex={codex.get('name')!r}")
    for label, market in (("claude", claude_market), ("codex", codex_market)):
        if name not in {p.get("name") for p in market.get("plugins", [])}:
            errors.append(f"{label} marketplace has no entry for plugin {name!r}")

    if "hooks" in codex:
        errors.append(".codex-plugin/plugin.json: remove 'hooks'; this repo ships skills only")
    if (ROOT / "hooks").exists():
        errors.append("hooks/: not allowed; Codex would auto-discover Claude-format hooks from it")


def run_external() -> None:
    if shutil.which("claude"):
        print("$ claude plugin validate . --strict")
        claude = subprocess.run(
            ["claude", "plugin", "validate", str(ROOT), "--strict"], check=False
        )
        if claude.returncode != 0:
            errors.append("claude plugin validate failed")
    else:
        warnings.append("claude not installed; skipped claude plugin validate")

    if CODEX_VALIDATOR.is_file():
        print(f"$ python {CODEX_VALIDATOR.name} .")
        result = subprocess.run(
            [sys.executable, str(CODEX_VALIDATOR), str(ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        # The Codex validator rejects `disable-model-invocation: true`, yet OpenAI's own
        # plugins (e.g. openai/plugins temporal) ship it and Codex loads them fine. Our
        # user-invoked skills need it for Claude, so that one complaint is ignored.
        problems = [
            line
            for line in result.stdout.splitlines()
            if line.startswith("- ") and "`disable-model-invocation` must be false" not in line
        ]
        for line in problems:
            errors.append(f"codex: {line[2:]}")
        if (
            result.returncode != 0
            and not problems
            and "Plugin validation failed" not in result.stdout
        ):
            errors.append(
                f"Codex validate_plugin.py failed: {result.stderr.strip() or result.stdout.strip()}"
            )
    else:
        warnings.append("Codex plugin-creator not installed; skipped Codex plugin validation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--external", action="store_true", help="also run harness validators")
    args = parser.parse_args()

    skill_dirs = (
        sorted(p for p in SKILLS.iterdir() if not p.name.startswith(".")) if SKILLS.is_dir() else []
    )
    stray = [p for p in skill_dirs if p.is_file()]
    for path in stray:
        errors.append(f"{path.relative_to(ROOT)}: only skill folders belong in skills/")
    total_desc = sum(check_skill(p) for p in skill_dirs if p not in stray)
    check_manifests()
    if args.external:
        run_external()

    for msg in warnings:
        print(f"warning: {msg}")
    for msg in errors:
        print(f"error: {msg}")
    count = len(skill_dirs) - len(stray)
    print(
        f"{count} skills, {total_desc} description chars loaded into every session, {len(errors)} errors"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
