# Scoped initialization and remediation

Read only for explicit init/update mode.

## Init

Discover the requested stack and purpose before scaffolding. If either is absent
and changes the result materially, ask; do not select a new product for the user.
Establish the applicable baseline using existing repository conventions:
- Purpose, prerequisites, local setup, verification, usage, and contact guidance.
- Documented configuration and a safe runnable sample when runtime config applies.
- Meaningful synthetic data or examples appropriate to the project.
- Applicable CLI contracts, logging/error behavior, version visibility, and tests.
- Relevant contribution and CI guidance without provisioning external resources.

Distinguish runnable samples from placeholders. Use temporary/local outputs for
checks and avoid production dependencies. If a sample needs credentials or an
external service, state that requirement and what was actually verified.

## Update

Inventory the requested gaps and impacted interfaces first. Apply only that scope.
A broad explicit “bring this project into alignment” request permits routine local
fixes across applicable categories, but still requires resolving breaking changes,
rule conflicts, and consequential product choices before proceeding.

Changing CLI names, exit codes, configuration transport, data formats, or release
behavior can break callers. Trace usage and propose a compatibility/migration path
before modifying them. Do not erase a deliberate existing exception or replace an
established framework just to make a checklist easier to satisfy.

Read documents before replacing content. Extend project guidance narrowly; do not
overwrite AGENTS.md/CLAUDE.md wholesale or add runtime rules to content-only repos.
When editing agent instructions, invoke an available agent-writing skill through
the harness's supported mechanism; report a required unavailable dependency.
Keep instructions harness-neutral and respect local instruction-file ownership.

## Verification and stopping

Use the repository's test and formatting commands. Test changed observable
contracts, including invalid configuration and failure exit codes where relevant.
Inspect CI syntax and conditions without triggering a release. Confirm examples
are runnable only when safe checks actually pass. Report environmental blockers
separately from guideline gaps.

Finish with a delta from the initial applicability matrix: fixed, unresolved,
accepted deviation, and unable to verify. Include changed paths and test results.
No implicit commit, push, deployment, credential changes, or external policy edits.
