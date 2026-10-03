# Skills repo: rules for agents and humans

One source of truth for Agent Skills used by Claude Code, Codex, Gemini CLI and any
other harness that reads the [Agent Skills spec](https://agentskills.io/specification).
`CLAUDE.md` is a symlink to this file.

## Layout

```
skills/<name>/                 one folder per shipped skill, flat (no nesting)
  SKILL.md                     the skill; the only file every harness reads
  agents/openai.yaml           Codex UI metadata + invocation policy
  references/ scripts/ assets/ loaded on demand
  evals/<case>/                `claude plugin eval` cases (prompt.md + graders/)
template/                      copy this to start a new skill (scripts/new-skill.sh)
.claude-plugin/                Claude Code plugin + single-plugin marketplace
.codex-plugin/plugin.json      Codex plugin manifest
.agents/plugins/marketplace.json  Codex marketplace pointing at this repo
scripts/                       new-skill.sh, link-skills.sh, validate.py, bump-version.sh
```

`skills/` holds only skills that ship. Drafts and retired skills live outside it, because
both plugin manifests point at `./skills/` as a whole and Codex drops symlinks when it
copies a plugin into its cache.

## Skill rules

- `name`: lowercase `a-z0-9-`, at most 64 chars, no leading, trailing or double `-`, equal to the folder name.
- `description`: at most 1024 chars, no `<` or `>`. Say what the skill does and when to use it.
  Every harness loads every description into every session, so keep it tight.
- Codex and Gemini read only `name` and `description`. Claude-only frontmatter (`allowed-tools`,
  `disable-model-invocation`, `context`, `model`, ...) is fine, but the skill must still work without it.
- Keep `SKILL.md` under 500 lines. Move detail to `references/`, one level deep.
- Every skill is either **model-invoked** (default) or **user-invoked**. A user-invoked skill sets both
  `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in
  `agents/openai.yaml`. `scripts/validate.py` fails if the two disagree.
- Invoke another skill through the current harness's supported skill mechanism, using its installed
  name (including a plugin namespace when required). If unavailable, report the dependency rather
  than assuming a tool exists. Never link into another skill's folder.
- Don't hard-code one harness's tool names in skill bodies. Describe the action ("read the file",
  "run the tests"). If a skill truly needs a per-harness mapping, put it in that skill's `references/`.
- Don't use `${CLAUDE_SKILL_DIR}` or other harness-only variables. Use paths relative to the skill folder.

## Not shared here

Subagents, slash commands, hooks and MCP config are not portable across harnesses, so this repo
ships skills only. The Codex manifest has no `hooks` field, and no `hooks/` directory may exist at
the repo root, because Codex would auto-discover Claude-format hooks from it.

## Workflow

| Task | Command |
|---|---|
| New skill | `scripts/new-skill.sh <name> [--user-invoked]` |
| Use locally (symlinks, edits apply live) | `scripts/link-skills.sh` (`--unlink` to remove) |
| Validate everything | `scripts/validate.py` |
| Test repo tooling | `uv run --with pyyaml python -m unittest discover -s tests -v` |
| Release | `scripts/bump-version.sh <x.y.z>` and commit |
| Behaviour test one skill | `cd skills/<name> && claude plugin eval` |

Every pull request that changes `skills/` or a manifest must bump the version. Claude and Codex only
deliver updates to plugin users when the version changes. CI enforces this.

## Install routes

Use **one** route per machine, never both: Codex lists a skill twice when it is visible
from two places.

- **Symlinks** (maintainers): `scripts/link-skills.sh` links each skill into `~/.claude/skills` and `~/.agents/skills`.
  Codex, Gemini CLI, Cursor, Copilot, OpenCode and Amp read `~/.agents/skills`. Antigravity's
  global folder is `~/.gemini/antigravity-cli/skills`, so pass `--antigravity` to add it.
- **Plugins** (everyone else): see `README.md`.
