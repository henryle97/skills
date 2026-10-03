---
max_turns: 16
---

Review this complete draft read-only with plan-review. The research notes below
are inline supplied evidence, not real files; cite their labels and sections.
The requested docs/postgres_performance.md is missing. Do not fetch new research.

Project requirement: a one-week prototype for one engineer; no speculative plugin
system. Acceptance criterion: duplicate delivery of an event has one effect.

Research note: software_architecture.md, section DRY: centralize duplicated domain
knowledge where the same rule must evolve together. Section YAGNI: defer extension
points without a current requirement. Section SOLID: interfaces may help isolate
volatile dependencies. There is no KISS section supplied.
Research note: python_threading.md, section Scope: these conclusions concern a
CPU-bound workload on a different runtime from this prototype. No benchmark for
this project is included.

Draft:
1. Create a plugin registry and interfaces for three hypothetical future backends.
2. Use worker threads because the research proves they always improve throughput.
3. Insert an event's output then mark the event handled in a separate transaction.
4. Test only the happy path. There is no user-facing UI.

Give the initial synthesis and decision questions, not a revised plan. If two
reviewers disagree about interfaces, explain the deciding requirement rather than
counting votes.
