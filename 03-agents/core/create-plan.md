---
name: create-plan
description: Generate a markdown execution plan with status tracking.
tools: inherit
model: inherit
domain: planning
---

# /create-plan - Execution Planning

Generate a markdown execution plan with status tracking.

**Tools in vault:** Plan templates in `05-templates/`. Save to `docs/plans/`. Use `project-planner` from `03-agents/core/` for complex breakdowns.

## Plan Creation Stage

Based on our full exchange, produce a markdown plan document.

### Requirements for the plan:

- Include clear, minimal, concise steps.
- Track the status of each step using these emojis:
  - 🟩 Done
  - 🟨 In Progress
  - 🟥 To Do
- Include dynamic tracking of overall progress percentage (at top).
- Do NOT add extra scope or unnecessary complexity beyond explicitly clarified details.
- Steps should be modular, elegant, minimal, and integrate seamlessly within the existing codebase.

### Markdown Template:

```markdown
# Feature Implementation Plan: {Task Name}

**Overall Progress:** `0%`

## TLDR
Short summary of what we're building and why.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: [choice] - [brief rationale]
- Decision 2: [choice] - [brief rationale]

## Tasks:

- [ ] 🟥 **Step 1: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

- [ ] 🟥 **Step 2: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

...
```

**Note:** It's still not time to build yet. Just write the clear plan document. No extra complexity or extra scope beyond what we discussed.
