---
name: plan
description: Create project plan using project-planner agent. No code writing - only plan file generation.
---

# /plan - Project Planning Mode

$ARGUMENTS

---

## 🔴 CRITICAL RULES

1. **NO CODE WRITING** - This command creates plan file only
2. **Use project-planner** from `03-agents/core/project-planner.md` - NOT Claude Code's native Plan subagent
3. **Socratic Gate** - Ask clarifying questions before planning
4. **Dynamic Naming** - Plan file named based on task

---

## Task

Use the `project-planner` agent with this context:

```
CONTEXT:
- User Request: $ARGUMENTS
- Mode: PLANNING ONLY (no code)
- Output: docs/plans/{task-slug}.md (dynamic naming)

NAMING RULES:
1. Extract 2-3 key words from request
2. Lowercase, hyphen-separated
3. Max 30 characters
4. Example: "e-commerce cart" → PLAN-ecommerce-cart.md

RULES:
1. Follow 03-agents/core/project-planner.md Phase -1 (Context Check)
2. Follow 03-agents/core/project-planner.md Phase 0 (Socratic Gate)
3. Create docs/plans/{slug}.md with task breakdown
4. DO NOT write any code files
5. REPORT the exact file name created
```

---

## Expected Output

| Deliverable | Location |
|-------------|----------|
| Project Plan | `docs/plans/{task-slug}.md` |
| Task Breakdown | Inside plan file |
| Agent Assignments | Inside plan file |
| Verification Checklist | Phase X in plan file |

---

## After Planning

Tell user:
```
[OK] Plan created: docs/plans/{slug}.md

Next steps:
- Review the plan
- Run `/create` or `/execute` to start implementation
- Or modify plan manually
```

---

## Naming Examples

| Request | Plan File |
|---------|-----------|
| `/plan e-commerce site with cart` | `docs/plans/ecommerce-cart.md` |
| `/plan mobile app for fitness` | `docs/plans/fitness-app.md` |
| `/plan add dark mode feature` | `docs/plans/dark-mode.md` |
| `/plan fix authentication bug` | `docs/plans/auth-fix.md` |
| `/plan SaaS dashboard` | `docs/plans/saas-dashboard.md` |

---

## Usage

```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
```
