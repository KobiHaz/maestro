---
name: review
description: Comprehensive code review task. Structured 7-step workflow with git scope, SOLID, removal candidates, security, and code quality. Uses specialists per code type. Adversarial mindset: must find issues.
---

# /review - Code Review Mode

Perform comprehensive code review with a structured 7-step workflow. Be thorough but concise.

## Place in the supply cycle

- **Stage:** **6 — Quality** (code review before branch close / merge).
- **Before:** **`/execute`** complete, tests passed, **`/document`** at least as required by lifecycle (or in parallel if policy allows).
- **After:** **`/finishing-branch`** (or fixes then repeat review).
- **Staffing:** specialists by code type — frontend / backend / security etc. from [[agent-routing]].

## Adversarial Review Rule (BMAD-inspired)

**You must find issues.** No "looks good" allowed. Adopt a skeptical stance — assume problems exist and find them.

- **Zero findings** → HALT. Re-analyze or explain why nothing was found.
- This is not negativity — it forces genuine analysis instead of rubber-stamping.
- Expect some false positives; user decides what's real. Present all findings with severity.

**Tools in vault:** Use specialists from `03-agents/specialists/` (frontend-specialist, backend-specialist, security-auditor) per code type. Load references from `03-agents/skills/code-review-checklist/`.

---

## 7-Step Workflow

### 1. Preflight — Scope Changes

- Use `git status -sb`, `git diff --stat`, and `git diff` to scope changes.
- If no files specified, scope via git diff (unstaged + staged).
- **No changes?** If `git diff` is empty, ask if user wants to review staged changes or a specific commit range.
- **Large diff (>500 lines)?** Summarize by file first, then review in batches by module/feature.

### 2. SOLID + Architecture

Load `03-agents/skills/code-review-checklist/solid-checklist.md` for prompts.

Check for:
- **SRP** — Overloaded modules, god objects
- **OCP** — Adding behavior requires editing core logic?
- **LSP** — Subclasses that break expectations
- **ISP** — Wide interfaces with unused methods
- **DIP** — High-level logic tied to low-level implementations

### 3. Removal Candidates

Load `03-agents/skills/code-review-checklist/removal-plan.md`.

Identify: unused code, redundant code, feature-flagged-off code.  
Distinguish: **safe delete now** vs **defer with plan**.  
If found, provide follow-up plan with steps and checkpoints.

### 4. Security Scan

Load `03-agents/skills/code-review-checklist/security-checklist.md`.

Check: XSS, injection, SSRF, auth gaps, secrets leakage, race conditions, weak crypto.  
For security-heavy changes: invoke `security-auditor` from `03-agents/specialists/`.

### 5. Code Quality

Load `03-agents/skills/code-review-checklist/code-quality-checklist.md`.

Check:
- **Error handling** — Swallowed exceptions, async errors, missing boundaries
- **Performance** — N+1 queries, CPU hotspots, missing cache, memory issues
- **Boundary conditions** — Null, empty collections, off-by-one, numeric limits

### 6. Output — Findings by Severity

Use P0–P3 format:

| Level | Name | Action |
|-------|------|--------|
| **P0** | Critical | Must block merge — security, data loss, correctness bug |
| **P1** | High | Should fix before merge — logic error, SOLID violation, perf regression |
| **P2** | Medium | Fix in this PR or create follow-up |
| **P3** | Low | Optional improvement — style, naming |

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

### P0 - Critical
(none or list)

### P1 - High
1. **[file:line]** Brief title
  - Description
  - Suggested fix

### P2 - Medium
...

### P3 - Low
...

## Removal/Iteration Plan
(if applicable)

## Next Steps

I found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**
1. **Fix all** — Implement all suggested fixes
2. **Fix P0/P1 only** — Address critical and high priority
3. **Fix specific items** — Tell me which to fix
4. **No changes** — Review complete, no implementation needed
```

### 7. Confirmation

**Do NOT implement changes until user explicitly confirms.**  
Review-first workflow. Present findings, then ask how to proceed.

---

## Legacy Quick Checks (Fallback)

If full workflow not needed:

- **Logging** — No `console.log`, proper logger with context
- **Error Handling** — Try-catch for async, centralized handlers
- **TypeScript** — No `any`, proper interfaces, no `@ts-ignore`
- **Production Readiness** — No debug, no TODOs, no hardcoded secrets
- **React/Hooks** — Effects cleanup, dependencies complete
- **Performance** — No unnecessary re-renders, memoization
- **Security** — Auth, input validation, RLS
- **Accessibility** — ARIA, WCAG 2.1
- **Architecture** — Existing patterns, correct directory
