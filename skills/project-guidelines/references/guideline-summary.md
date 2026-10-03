# Source provenance and applicability routing

Default source: [coding-guidelines.md](coding-guidelines.md), a generic export
last updated on **2026-10-03**.
SHA-256: `c48c97de71d3c226a6294688aa6b8b536c93985f55ae05119006ed33e13098b1`.

The bundled export works offline and is the default authority for this skill. A user explicitly
supplying another local guideline file selects that file for the review. Do not
call Outline or automatically refresh this copy. Synchronizing a new export is an
explicit maintenance task; update this date/hash when replacing it.

External links are not bundled
source material and are not automatically fetched.

## Coverage routing

Read shared guidance and only the language-specific sections applicable to the
project. Build the applicability matrix across these source sections:

- Configuration, Logging, —specs, Exit Code.
- UI/UX, Framework, Project Documents, Versioning, Testing.
- C++ (Basic Requirements, Coding Style, Design Principles, minor notes, Bazel
  Project Structure), Python, Go, Bash, HDL, Javascript (or Frontend).
- Google Docs when the reviewed work includes that document format.
- Git, Gitlab CICD.

The export targets the majority of firm applications, not all possible projects.
Cite the actual source section for each finding; this routing guide is not a
second policy or a substitute for reading the Markdown export.

## Applicability cautions

- UI includes CLI, but monitor/phone layout checks concern graphical interfaces.
  Physical screen size alone does not establish CSS viewport requirements.
- Non-executable packages need suitable documentation and examples, not an
  invented runtime application. Explain the equivalence and scope judgment.
- Executable --specs declarations require project evidence for resource estimates;
  example resource values do not establish a workload's needs.
- Testing guidance is risk- and project-stage-sensitive; do not convert examples
  into blanket test-count or coverage requirements.
- Language/toolchain/version choices in the export are policy statements to
  assess, not claims that a dependency is current or suitable for every project.
  Surface conflicts with local instructions rather than silently installing tools,
  changing frameworks, or weakening safety. Preserve the distinction between the
  source's Python formatting advice and the repository's supported lint workflow.
- Git default branches, canonical release hosts, and server capabilities need
  local evidence. Source examples do not authorize renaming main to master,
  changing deploy keys, or running release jobs.
- Configuration compliance must preserve secret handling; examples use synthetic
  data and never real credentials or production records.
