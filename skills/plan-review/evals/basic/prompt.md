---
max_turns: 16
---

Use plan-review to review this complete implementation-plan draft. Work read-only.
There are no project research documents available for this exercise. Do not fetch
new research. Use independent reviewers if available and disclose limitations.

Goal: a small internal CSV-import API. Acceptance criteria: retries never duplicate
records, malformed rows are reported, and import status can be queried. Non-goals:
a dashboard and a new deployment platform.

Plan:
1. Add a POST /imports endpoint and a GET /imports/{id} status endpoint.
2. Launch an in-process worker thread to parse every uploaded CSV into memory.
3. Insert rows one at a time; on request retry, start a new import.
4. Keep import status in process memory. Deploy by restarting the application.
5. Test the successful import of a ten-row file.

Review the plan, then ask me the first round of consequential decisions. Do not
rewrite the plan yet or start implementation.
