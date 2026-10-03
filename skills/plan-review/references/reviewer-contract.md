# Shared reviewer contract

The coordinator includes this contract in every specialist assignment.

## Assignment

Review the frozen plan solely through your assigned lens. Read the supplied project
requirements, repository rules, and relevant reference sections. Inspect narrowly
relevant local context read-only when necessary. Stay within the chosen project,
constraints, and non-goals; report adjacent concerns to the coordinator rather than
repeating another role's whole review.

Tighten the plan with the smallest useful change. Test proposed corrections against
cost, complexity, and the user's goals. Principles are diagnostic lenses, not
mandatory patterns. Do not invent implementation facts, workloads, source passages,
or a finding quota. Silence is better than a generic checklist.

## Return

State applicability, sources actually read, evidence gaps, and up to five
consequential findings, ranked by severity. For each finding include:
- **ID and severity:** role-local ID; blocker, major, or minor. A blocker prevents
  a stated acceptance criterion or creates an unacceptable unresolved risk; major
  means a consequential likely failure or expensive rework; minor is bounded.
- **Plan anchor:** quoted passage or stable section/line reference.
- **Evidence:** concrete document path and section/lines, applicable project rule,
  or explicitly labeled inference. Explain the connection, not just the citation.
- **Consequence:** a project-specific failure scenario, including assumptions.
- **Correction:** smallest useful amendment, its cost, and why it improves the plan.
- **Confidence:** high, medium, or low, with the missing fact when conditional.
- **Decision:** question for the user only if a consequential choice remains.

Finish with what to keep and unresolved questions. If a role is inapplicable,
explain why. If applicable but no consequential finding is supported, say so and
state the coverage limits. Missing evidence is not proof that the plan is sound.
