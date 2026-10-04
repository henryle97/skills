# Shared reviewer contract

The coordinator includes this contract in every specialist assignment.

## Assignment

Review the frozen plan solely through your assigned lens or lenses. Work from the
packet: its requirements, repository rules, and reference excerpts. Do not re-read
repository guidance the packet already summarizes. Open code or sources read-only
only to check a specific claim the packet cannot settle. Stay within the chosen project,
constraints, and non-goals; report adjacent concerns to the coordinator rather than
repeating another role's whole review.

Tighten the plan with the smallest useful change. Test proposed corrections against
cost, complexity, and the user's goals. Principles are diagnostic lenses, not
mandatory patterns. Do not invent implementation facts, workloads, source passages,
or a finding quota. Silence is better than a generic checklist.

## Return

Keep the return short. State applicability, sources actually read, evidence gaps,
and at most three consequential findings per lens, ranked by severity. Report only
findings you score 80 or higher. A consequential concern that scores lower only
because it hinges on a missing fact goes under unresolved questions, naming that
fact. For each finding include, one or two lines each:
- **ID and severity:** role-local ID; blocker, major, or minor. A blocker prevents
  a stated acceptance criterion or creates an unacceptable unresolved risk; major
  means a consequential likely failure or expensive rework; minor is bounded.
- **Plan anchor:** quoted passage or stable section/line reference.
- **Evidence:** concrete document path and section/lines, applicable project rule,
  or explicitly labeled inference. Explain the connection, not just the citation.
- **Consequence:** a project-specific failure scenario, including assumptions.
- **Correction:** smallest useful amendment, its cost, and why it improves the plan.
- **Confidence:** a 0–100 score from the rubric below, with the missing fact when
  conditional.
- **Decision:** question for the user only if a consequential choice remains.

Confidence rubric:
- **0:** a false positive under light scrutiny, or outside the plan's scope.
- **25:** might be real; not verified against the plan or evidence, or a stylistic
  preference no project rule calls out.
- **50:** verified but minor or unlikely to matter for this project.
- **75:** verified against the plan and evidence, likely to bite in practice, or
  directly required by a project rule.
- **100:** certain; the plan passage and evidence directly confirm it.

Finish with what to keep and unresolved questions. If a role is inapplicable,
explain why. If applicable but no consequential finding is supported, say so and
state the coverage limits. Missing evidence is not proof that the plan is sound.
