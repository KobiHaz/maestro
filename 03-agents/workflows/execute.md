---
name: execute
description: Implement the plan step by step precisely as planned.
---

# /execute - Implementation Mode

Implement the plan precisely as planned, in full.

**Tools in vault:** Agents from `03-agents/specialists/` (frontend-specialist, backend-specialist, test-engineer per plan). Plan file in `docs/plans/`. Document workflow: `03-agents/workflows/document.md`.

## Implementation Requirements:

- Write elegant, minimal, modular code.
- Adhere strictly to existing code patterns, conventions, and best practices.
- Include thorough, clear comments/documentation within the code.
- As you implement each step:
  - Update the markdown tracking document (e.g., `PLAN-{slug}.md`) with emoji status and overall progress percentage dynamically.
  - Report status after each phase/step.

// turbo
1. Identify the active PLAN markdown file.
2. Execute the next 🟥 task/subtask.
3. Update status to 🟨 while working and 🟩 when complete.
4. Recalculate and update the overall progress percentage.

## Completion (MANDATORY)

When all tasks are done:

1. **Document** — Run `03-agents/workflows/document.md`: update or create documentation for the changes
2. **Delete plan** — Remove the plan file from docs/plans/ (no persistence needed)
3. **Log** — Add entry to 07-logs/ if significant
