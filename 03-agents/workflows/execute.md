---
name: execute
description: Implement the plan step by step precisely as planned.
---

# /execute - Implementation Mode

Implement the plan precisely as planned, in full.

## Place in the supply cycle

- **Stage:** **3 — Execution** (implement tasks per plan in `docs/plans/*`).
- **Before:** **`/plan`** — a plan with staffing from `03-agents/...` is required (see [[agent-routing]]).
- **After:** **tests** (Verification below + **`/test`** as needed) → **`/document`** → **`/review`** → **`/finishing-branch`** (do not skip lifecycle in `plans-and-tasks.md`).

**Tools in vault:** Agents from `03-agents/specialists/` (frontend-specialist, backend-specialist, test-engineer per plan). Document workflow: `03-agents/workflows/document.md`.

### Not duplicate of `/enhance`

| | **`/execute` (this workflow)** | **`/enhance`** (`workflows/enhance.md`) |
|--|----------------------------------|----------------------------------------|
| **Source of truth** | Active **`docs/plans/*.md`** with 🟩🟨🟥 (and sync to `plans-and-tasks.md`) | Ad-hoc request (`$ARGUMENTS`); optional informal mini-plan |
| **Discipline** | Step-by-step plan updates, mandatory verification, plan-lifecycle completion | Iterative “add feature”; user approval for big changes |
| **When** | Maestro flow after planning | Quick iteration when no formal plan file |

## Plan artifacts (two layers — do not confuse them)

| Artifact | Role |
|----------|------|
| `02-projects/<project>/plans-and-tasks.md` | **Project source of truth** for open work, milestones, and what “done” means for that repo. Update when scope or priorities shift. |
| `docs/plans/*.md` (emoji 🟩🟨🟥, optional `PLAN-*.md` naming) | **Ephemeral execution plan** for the current slice: step-by-step tracking while implementing. |

**During `/execute`:** Read and update the active file under `docs/plans/` (progress, emojis). **Do not** let task state live only there if the project already tracks work in `plans-and-tasks.md` — keep that file aligned (same done/open story) before you finish.

**When finishing:** Run the completion checklist below (sync `plans-and-tasks.md`, then remove the ephemeral plan). Full rules: [[04-knowledge/standards/maestro-project-doc-lifecycle]].

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

## Verification Before "Done" (MANDATORY)

Before declaring completion:

- [ ] Run `npm run test` (or project test command) — tests pass
- [ ] Run `npm run build` — build succeeds
- [ ] Run `npm run lint` (or `npx tsc --noEmit`) — no errors

**Do not claim "done" without running verification.** Evidence before assertions.

## Completion (MANDATORY — Do Not Skip)

When all tasks are done and verified, run **plan-lifecycle** completion checklist:

1. **plans-and-tasks** — Update `02-projects/<project>/plans-and-tasks.md`: what done, what open
2. **Document** — Run `03-agents/workflows/document.md`: CHANGELOG, project brief, 04-knowledge if relevant
3. **Delete plan** — Remove plan file from `docs/plans/` or `02-projects/<project>/` (no persistence)
4. **Log** — Add entry to `07-logs/` if significant
5. **Next** — Suggest `/review` (code review, mandatory) then `/finishing-branch` for merge/PR/cleanup

> 🔴 **Flow:** Execute complete → `/review` (adversarial) → resolve findings → `/finishing-branch`

Details: [[04-knowledge/standards/maestro-project-doc-lifecycle]]
