---
name: finishing-branch
description: When implementation is complete — verify tests, present merge/PR options, cleanup worktree. Use after /execute completes or when all tasks are done.
---

# /finishing-branch - Complete Development Branch

When all implementation tasks are done, use this workflow to close out the branch safely.

## Place in the supply cycle

- **Stage:** **6 — Close-out** (final verification, merge/PR options, cleanup).
- **Before:** **`/review`** (or explicit decision to skip — Maestro default: do not skip).
- **After:** merge / PR / delete ephemeral plan from `docs/plans/*` per [[04-knowledge/standards/maestro-project-doc-lifecycle]].
- **Staffing:** `test-engineer` for verification; other actions per project.

**Tools in vault:** `03-agents/specialists/test-engineer` for verification. Git, project commands from `02-projects/` if available.

---

## When to Use

- All tasks in plan are marked complete
- After `/execute` has finished
- Before merging to main or opening PR

**Not for:** Deploy to production (use `/deploy`).

---

## Steps

### 0. Code Review (MANDATORY before merge)

- [ ] Run `/review` — comprehensive code review with adversarial mindset
- [ ] **Adversarial rule:** Review must produce findings. Zero findings → re-analyze or explain why.
- [ ] Resolve or acknowledge all P0/P1 findings before proceeding
- [ ] If user chooses "Open PR", external review may follow; internal review still required first

### 1. Verify

- [ ] Run `npm run test` (or project test command)
- [ ] Run `npm run build`
- [ ] Lint: `npm run lint` or `npx tsc --noEmit`
- [ ] If failures: Stop. Fix before proceeding.

### 2. Document — Plan-Lifecycle Checklist (MANDATORY if not yet done)

Before merge/PR, verify:

- [ ] **plans-and-tasks.md** — What was done, what remains open
- [ ] **Documentation** — CHANGELOG, project brief, 04-knowledge if relevant
- [ ] **Plan file deleted** — From docs/plans/ or 02-projects/<project>/
- [ ] **07-logs/** — Entry if significant

Run `03-agents/workflows/document.md`. Details: [[04-knowledge/standards/maestro-project-doc-lifecycle]]

### 3. Present Options

Ask user:

```
All tasks complete. Tests pass. How would you like to proceed?

1. **Merge** — Merge to main (or target branch)
2. **Open PR** — Create pull request for review
3. **Keep branch** — Continue work or hold for later
4. **Discard** — Abandon changes, reset branch

Which option?
```

### 4. Execute Choice

- **Merge**: Guide user through merge (or perform if authorized)
- **PR**: Help draft PR description, link to plan/CHANGELOG
- **Keep**: Confirm branch name, remind of plan file location
- **Discard**: Confirm, then `git reset --hard` to target (with user confirmation)

### 5. Cleanup (if merge/discard)

- Delete plan file from `docs/plans/` or `02-projects/<project>/` if merged
- Remove worktree if using git worktrees
- Log significant completions in `07-logs/`

**Reminder:** If documentation/plan-lifecycle was skipped earlier, complete it before cleanup.

---

## Safety

- **Never force push** to shared branches without explicit user confirmation
- **Always confirm** before destructive operations (discard, reset)
- **Document first** — Ensure changes are documented before merge
