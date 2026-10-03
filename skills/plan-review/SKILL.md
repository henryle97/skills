---
name: plan-review
description: Review a complete implementation-plan draft before approval with eight evidence-grounded specialist subagents, then grill the user on consequential trade-offs. Use when a drafted plan is ready for review or the user requests plan review; not for early brainstorming or reviewing implemented code.
---

# Plan Review

Turn a draft into explicit, defensible decisions. Review the plan, not imaginary
implementation details. Keep review read-only; propose revisions after agreement,
and edit a plan file only on an explicit request. Review readiness never authorizes
implementation, external actions, or expanding the user's scope.

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
   repository. Record concrete paths and relevant sections for each specialist.
   Report missing evidence; new research requires a separate user request.
4. Freeze the draft for this review round. Give every reviewer the same numbered
   plan passages or stable file lines, requirements, constraints, and non-goals.

## Run eight independent reviews

Read [references/specialists.md](references/specialists.md) for the eight role
prompts and [references/reviewer-contract.md](references/reviewer-contract.md)
for their shared evidence and output contract.

Launch one subagent per role, with its role prompt, the shared contract, the frozen
plan, project constraints, applicable repository rules, and its explicit reference
map. Give each reviewer access to the assigned documents, not just filenames.
Ask them to read the relevant sections before judging the plan. Reviewers inspect
read-only and do not delegate further or receive other reviewers' conclusions.

Use parallel execution where supported; otherwise batch within the harness's
concurrency limit. Collect and release completed agents before opening another
batch. If delegation is unavailable or prohibited, disclose the limitation and
provide eight labeled local passes only as a fallback, not independent reviews.
Report failed or incomplete roles rather than claiming eight completed reviews.

Keep all eight roles. A role outside the project's scope returns “not applicable”
with its reason; it does not invent work to justify its seat. One initial full
review is the default. Subsequent review is limited to affected roles and material
changes, not automatic repetition after every answer.

## Consolidate before grilling

Check each finding against its cited plan passage, project constraint, and source
section. Remove misreadings, unsupported factual claims, and generic preferences.
Merge duplicate consequences while retaining specialist provenance. Keep
contradictions visible: resolve them against requirements and evidence, not votes.
Research is evidence, not authority overriding project requirements.

Present a concise initial synthesis:
- Scope and reference gaps, including incomplete reviewer coverage.
- What to keep and why it fits the project.
- Ranked consequential findings and their smallest useful corrections.
- Conflicting recommendations and the trade-off that separates them.

## Grill the decision frontier

Map unresolved decisions and their prerequisites. Ask only questions whose
prerequisites are settled; ask the whole current frontier in a numbered round,
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
change the plan, propose a targeted review of the affected roles and explain why.

## Finish

Propose a revised draft or focused amendments incorporating only agreed decisions.
When the user requests file edits, preserve unrelated content. Report:
- Agreed changes and preserved choices.
- Remaining risks, assumptions, evidence gaps, and deferred decisions.
- Readiness: **ready**, **ready with accepted risks**, or **not ready**, grounded
  in the project's acceptance criteria and unresolved blockers.

Make limited reviewer coverage explicit. Do not portray absent evidence as verified
safety or treat a review as permission to begin implementation.
