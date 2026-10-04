---
name: plan-review
description: Review a complete implementation-plan draft before approval with evidence-grounded specialist lenses, scaled to the plan's size and risk, then grill the user on consequential trade-offs. Use when a drafted plan is ready for review or the user requests plan review; not for early brainstorming or reviewing implemented code.
---

# Plan Review

Turn a draft into explicit, defensible decisions. Review the plan, not imaginary
implementation details. Keep review read-only; propose revisions after agreement,
and edit a plan file only on an explicit request. Review readiness never authorizes
implementation, external actions, or expanding the user's scope.

Cost discipline: gather context once, spawn reviewers only for lenses that apply,
and keep only findings that survive a confidence filter.

## Establish the review packet

1. Locate the complete draft in the conversation or a user-selected file. If there
   are competing drafts, establish which one is authoritative. If no draft exists,
   ask for it rather than drafting a different project.
2. Read repository guidance and enough local context to establish the goal,
   stack, constraints, acceptance criteria, and non-goals. Separate requirements,
   choices, assumptions, and unknowns. Ask only for consequential facts unavailable
   locally. Missing plan detail is a question, not evidence of a defective design.
3. Build a reference map using [references/evidence.md](references/evidence.md).
   Prefer user-provided paths, then relevant research documents in the current
   repository. Report missing evidence; new research requires a separate user request.
4. Freeze the draft into one self-contained packet: numbered plan passages,
   requirements, constraints, non-goals, applicable repository rules, and the
   **excerpted text** of relevant reference sections (not only paths). Reviewers
   work from this packet, so the coordinator reads each source once instead of
   every reviewer rediscovering it.

## Triage lenses and pick the review size

[references/specialists.md](references/specialists.md) defines eight lenses:
architecture, coding standards, UI/UX, performance, security, data and
correctness, testing, operations. Mark each **applicable** or **not applicable**
with a one-line reason from the packet. A not-applicable lens gets no reviewer.

Then size the review from the plan, unless the user names a level:

| Size | When | Reviewers |
|---|---|---|
| **small** | Short plan, prototype, single module, low blast radius | One local pass per applicable lens group, no subagents |
| **standard** (default) | Typical feature or service change | One subagent per applicable lens group below (usually 3–4) |
| **full** | Large, cross-team, production data or security critical, or user asks | One subagent per applicable lens (up to 8) |

Lens groups for standard size: **Design** (architecture + coding standards),
**Correctness** (data and correctness + testing), **Risk** (security + operations),
**Performance**, **UI/UX**. Drop a group whose lenses are all not applicable.

State the chosen size and the triage table in the synthesis.

## Run the reviews

Give each reviewer its lens prompt(s) from `references/specialists.md`, the
shared contract in [references/reviewer-contract.md](references/reviewer-contract.md),
and the frozen packet. Reviewers inspect read-only, stay inside their lenses, do
not delegate further, and do not see other reviewers' conclusions. They read code
or source files only to check a specific claim the packet cannot settle.

Where the harness lets you choose a model per subagent, run reviewers on a faster,
cheaper tier and keep the coordinator on the main model. Launch all reviewers in
parallel where supported; otherwise batch within the concurrency limit. If
delegation is unavailable, disclose it and do labeled local passes instead.
Report failed or incomplete reviewers rather than claiming full coverage.

Invoke the `project-guidelines` skill only when the user asked for firm-guideline
compliance; otherwise the coding-standards lens uses the repository rules already
in the packet.

## Consolidate before grilling

Drop findings below confidence 80 (see the contract's rubric). Re-check only the
remaining blockers and majors against their cited plan passage and source excerpt;
remove misreadings, unsupported claims, and generic preferences. Merge duplicate
consequences while keeping lens provenance. Keep contradictions visible and resolve
them against requirements and evidence, not votes. Research is evidence, not
authority overriding project requirements.

Present a concise initial synthesis:
- Review size, lens triage (all eight, with not-applicable reasons), and reference
  gaps or incomplete coverage.
- What to keep and why it fits the project.
- Ranked consequential findings and their smallest useful corrections.
- Conflicting recommendations and the trade-off that separates them.

## Grill the decision frontier

Map unresolved decisions and their prerequisites. Ask only questions whose
prerequisites are settled, at most five per round, most consequential first,
then wait. Questions dependent on unanswered choices belong to the next round.

For each question give:
- A short title and the precise decision needed.
- The plan assumption being challenged, evidence, and consequence.
- The meaningful alternatives and a recommended answer with its trade-off.

Challenge whether a recommendation actually serves this project's goals before
asking the user to adopt it. Grill consequential uncertainty, not every suggestion
or stylistic preference. Accept a reasoned risk or deliberate non-goal; reviewers
are advisers, not an approval committee. Recompute the frontier after answers and
keep a concise decision ledger. Stop when decisions are settled or the user asks
to stop; at a stop, disclose what remains unresolved. If answers fundamentally
change the plan, propose re-running only the affected lenses and explain why.

## Finish

Propose a revised draft or focused amendments incorporating only agreed decisions.
When the user requests file edits, preserve unrelated content. Report:
- Agreed changes and preserved choices.
- Remaining risks, assumptions, evidence gaps, and deferred decisions.
- Readiness: **ready**, **ready with accepted risks**, or **not ready**, grounded
  in the project's acceptance criteria and unresolved blockers.

Make limited reviewer coverage explicit. Do not portray absent evidence as verified
safety or treat a review as permission to begin implementation.
