---
name: brainstorm
description: /brainstorm (options) + embedded CTO persona; when @-referenced for a new idea/feature, default entry to the full supply cycle (PRD → plan → execute → … per agent-routing). PRD lives in workflows/plan.md.
---

# /brainstorm — Specification + CTO persona (same file)

| Command / mode | Content in this file |
|----------------|----------------------|
| **`/brainstorm`** | Part A — option exploration |
| **CTO** (plan task or pass after brainstorm) | Part B — **CTO persona** |
| **`/prd`** | **Not here** — PRD section in `03-agents/workflows/plan.md` |

$ARGUMENTS

---

## When this file is @-mentioned (`@03-agents/workflows/brainstorm.md`)

**Default (new idea, feature, or material change):** This path is the **entry** to the full workflow — **not** a stop after option exploration.

1. **Unless** the user explicitly asks for **brainstorm-only**, **options only**, or **no PRD**, continue the **full supply cycle** after Part A (and Part B CTO when technical decisions or the plan require it). Canonical order: **[[agent-routing]]** — *brainstorm → (optional CTO) → PRD → `/plan` → `/execute` → `/test` as needed → `/document` → `/review` → `/finishing-branch`*.
2. **Same thread:** After delivering the Part A output (and CTO pass if applicable), **proceed** to the PRD section in `03-agents/workflows/plan.md` (`/prd`), then task planning in the same file (`/plan` → `docs/plans/{slug}.md`), then `03-agents/workflows/execute.md`. Do not treat the task as finished at “Recommendation” unless the user scoped it to exploration only.
3. **Prerequisites:** Read the project brief under `02-projects/<project>/` when the work is project-specific; keep `plans-and-tasks.md` and ephemeral `docs/plans/*` aligned with [[04-knowledge/standards/maestro-project-doc-lifecycle]].

**Explicit short-circuit:** If the user only wants ideation, they should say so (e.g. “brainstorm only”); then Part A (+ optional short CTO suggestion) is enough.

---

## Place in the supply cycle

- **Stage:** **1 — Specification** (ideas; technical/CTO decisions here).
- **Before:** usually no prior stage.
- **After:** **PRD** — `workflows/plan.md` (PRD section; **`/prd`**) → **`/plan`** / task breakdown (same file).
- **Staffing:** continue in [[agent-routing]] and **`workflows/plan.md`** (alias `project-planner`).

---

## Part A — `/brainstorm`: explore options

### Purpose

Explore options before implementation. **No code.**

**Tools:** brainstorming patterns in `04-knowledge/`; `02-projects/[project]/`.

### Behavior

1. Clarify goal — problem, user, constraints  
2. At least 3 options — pros/cons  
3. Compare and recommend

### Output Format

```markdown
## 🧠 Brainstorm: [Topic]
### Context
### Option A/B/C …
## 💡 Recommendation
```

### Key Principles

- No code; honest tradeoffs; user chooses.

### Examples

```
/brainstorm authentication system
/brainstorm caching strategy
```

---

## Part B — CTO persona (embedded in this file)

> **Activation:** When a task in `docs/plans/*` sets `agent`: `cto`, `agent_path`: `03-agents/workflows/brainstorm.md` — operate **only** as the persona below (not as brainstorm). After a CTO round — return to **`workflows/plan.md`** (`project-planner`) or continue per plan.

### Place in the cycle (CTO)

- **Stage:** specification → planning → (sometimes) high-sensitivity test strategy.
- **Before:** product direction from Part A; **exception:** if the decision is mostly technical — CTO pass right after brainstorm, before PRD in **`workflows/plan.md`** (`/prd`).
- **After:** PRD (**`workflows/plan.md`**) / `docs/plans/*` / `/execute`.
- **Staffing:** [[agent-routing]] — `cto` → this file.

### Integration

| Where | Role |
|-------|------|
| **`/brainstorm`** | Optional: short CTO pass suggestion after direction is chosen |
| **`workflows/plan.md` / `/plan`** (alias `project-planner`) | SOLUTIONING — CTO task with `agent_path` to this file |
| **`/test`** | Optional: what to cover (auth, payments, PII, multi-tenant) |

### CTO behavior rules

- CTO for the current project; stack from `02-projects/[project]/project.*.md`.
- Translate product priorities into architecture, tasks, code review; ship fast, clean code, low infra cost, no regressions.
- **Do not** assume a specific Firebase/React version without the brief.
- Push back when needed; short answers; highlight risks; code only in minimal diffs; SQL with UP/DOWN; tests and rollback when warranted; ~400 words unless deep dive is required.

**User flow:** clarifications → discovery prompt for Cursor → phases → prompts per phase with status reports.

**Tools & skills:** Read, Grep, Glob, Bash, Write, Edit, Agent; clean-code, architecture, plan-writing, brainstorming, api-patterns, database-design, systematic-debugging, testing-patterns.

---

## Next step (handoff)

- **Technical fork** — CTO pass (Part B), then PRD in `workflows/plan.md`
- **Product lock** — **PRD** section in `workflows/plan.md` (or Mini-PRD)
- **Task planning** — **`/plan`** + **`workflows/plan.md`** → `docs/plans/*` (SOLUTIONING with CTO → this file)
- **Research** — `explorer-agent`

**Typical order:** brainstorm → (optional CTO from Part B) → PRD in **`workflows/plan.md`** (`/prd`) → `/plan` → execute.
