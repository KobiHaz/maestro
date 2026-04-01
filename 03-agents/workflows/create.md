---
name: create
description: Create new application command. Triggers App Builder skill and starts interactive dialogue with user.
---

# /create - Create Application

$ARGUMENTS

---

## Place in the supply cycle

- **Stage:** **3 (special) — new application** — still needs product spec/direction before full build; usually after `brainstorm` and/or PRD in `workflows/plan.md` or explicit user decision.
- **Before:** like a large feature — prefer a short spec; **`/plan`** (`workflows/plan.md`) before or as part of the process (see steps below).
- **After:** same path as normal execution — tests, documentation, review, finishing-branch (see [[agent-routing]]).
- **Staffing:** specialists (DB, backend, frontend, …) from [[agent-routing]] per chosen stack and plan.

---

## Task

**Tools in vault:** `03-agents/`, `04-knowledge/`. Preview from `03-agents/scripts/` if present. Otherwise: `npm run dev`, project brief from `02-projects/[project]/`.

This command starts a new application creation process.

### Steps:

1. **Request Analysis**
   - Understand what the user wants
   - If information is missing, use `conversation-manager` skill to ask

2. **Project Planning**
   - Use **`/plan`** / `03-agents/workflows/plan.md` for task breakdown
   - Determine tech stack
   - Plan file structure
   - Create plan file and proceed to building

3. **Application Building (After Approval)**
   - Orchestrate with `app-builder` skill
   - Coordinate expert agents:
     - `database-architect` → Schema
     - `backend-specialist` → API
     - `frontend-specialist` → UI

4. **Preview**
   - Run `npm run dev` when complete
   - Present URL to user

---

## Usage Examples

```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## Before Starting

If request is unclear, ask these questions:
- What type of application?
- What are the basic features?
- Who will use it?

Use defaults, add details later.
