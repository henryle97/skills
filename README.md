# Henry Skills

Reusable agent skills for Codex, Claude Code, and other compatible tools.

## Main plugin skills

<details>
<summary><h4>plan-review</h4></summary>

Review a draft implementation plan with eight specialists, then work through the
key decisions before revising it. Read-only by default.

[Skill instructions](skills/plan-review/SKILL.md)

</details>

<details>
<summary><h4>project-guidelines</h4></summary>

Review, initialize, or update a project against the bundled Coding Guidelines using
the bundled Markdown export. Review is read-only by default.

[Skill instructions](skills/project-guidelines/SKILL.md)

</details>

<details>
<summary><h4>grilling</h4></summary>

Stress-test a plan, decision, or idea with rounds of numbered questions, each with
a recommended answer, until every branch of the decision tree is settled.
From [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).

[Skill instructions](skills/grilling/SKILL.md)

</details>

<details>
<summary><h4>handoff</h4></summary>

Compact the current conversation into a handoff document so a fresh agent can
continue the work. User-invoked only.
From [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).

[Skill instructions](skills/handoff/SKILL.md)

</details>

## Install

Choose **one route per machine** to avoid duplicate skills. Repository access and
an SSH key configured for GitHub are required.

### Local checkout

```bash
git clone git@github.com:henryle97/skills.git ~/src/henry-skills
cd ~/src/henry-skills
scripts/link-skills.sh
```

Links skills into `~/.agents/skills` and `~/.claude/skills`. Update with
`git pull --ff-only`; remove links with `scripts/link-skills.sh --unlink`.

### Codex plugin

```bash
codex plugin marketplace add git@github.com:henryle97/skills.git
codex plugin add henry-skills@henry
```

If your Codex version does not support plugin commands, use the local checkout.

### Claude Code plugin

Run inside Claude Code:

```text
/plugin marketplace add git@github.com:henryle97/skills.git
/plugin install henry-skills@henry
```

## Use

Select the installed skill in your tool, or invoke it by its installed name:

```text
$plan-review Review docs/plan.md and grill me on the key decisions.
$project-guidelines Review this repository. Do not edit files.
```

Plugin installations may include a namespace. See each skill's instructions
for details; reviews are read-only by default.

## Contribute

See [AGENTS.md](AGENTS.md) for authoring rules, validation, and releases.
Run `uvx pre-commit install` once per clone; the hook blocks commits containing
API keys, credentials, or private keys (gitleaks). CI scans the full history too.
Use feature branches and open a PR against `main`. Maintainer: `@henry`.
