---
max_turns: 12
---

Use project-guidelines in review mode for this supplied project description.
Use the bundled local Markdown guideline export and identify that source.
Do not call Outline or refresh the export.
Do not browse or modify files. The supplied information is all the available
implementation evidence.

A per-date data-processing CLI currently accepts --config, --date, and --specs.
It reads YAML with snake_case fields. A safe sample config and synthetic CSV
fixture exist, but neither has been executed. --specs declares JSON inputs,
outputs, cpu.cores, cpu.memory_mb, and gpu.memory_mb. Logging includes timezone,
thread ID, and source location and is best-effort. Invalid configuration exits 1.
README explains purpose and local setup. Release jobs run on both a canonical
GitLab host and its mirror. Default branch is main. There is no graphical UI.

Give an applicability-aware report, prioritize corrections, and explain what
cannot be verified. Do not fix anything or rename the default branch.
