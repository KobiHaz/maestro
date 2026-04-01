---
name: document
description: Update documentation after code changes. MANDATORY after plan execution.
---

# /document - Documentation Update Mode

Identify and update documentation after code changes. **Required after every plan execution** — if no docs exist, create them.

## Place in the supply cycle

- **Stage:** **5 — Documentation** (CHANGELOG, README, vault knowledge — per what actually changed).
- **Before:** execution + basic verification (tests); otherwise docs may describe code that does not hold.
- **After:** **`/review`** (code review) then **`/finishing-branch`** as needed.
- **Staffing:** `documentation-writer` from [[agent-routing]] for heavy documentation.

**Tools in vault:** `03-agents/specialists/documentation-writer`, templates in `04-knowledge/` or `05-templates/`.

## 1. Identify Changes
- Check git diff or recent commits for modified files.
- Identify which features/modules were changed.
- Note any new files, deleted files, or renamed files.

## 2. Verify Current Implementation
**CRITICAL**: DO NOT trust existing documentation. Read the actual code.

For each changed file:
- Read the current implementation.
- Understand actual behavior (not documented behavior).
- Note any discrepancies with existing docs.

## 3. Update Relevant Documentation

- **CHANGELOG.md**: Add entry under "Unreleased" section.
  - Use categories: Added, Changed, Fixed, Security, Removed.
  - Be concise, user-facing language.
- Update project codebase docs (CODEBASE.md if exists, else README) if repository structure or core logic changed. Use documentation-writer from `03-agents/specialists/` for complex docs.
- **Audits/reports:** Update vault only (`04-knowledge/reference/<project>-*`, `06-outputs/`, `07-logs/`). Do not keep audit/performance reports in project `docs/`.

## 4. Documentation Style Rules

✅ **Concise** - Sacrifice grammar for brevity.
✅ **Practical** - Examples over theory.
✅ **Accurate** - Code verified, not assumed.
✅ **Current** - Matches actual implementation.

❌ No enterprise fluff.
❌ No outdated information.
❌ No assumptions without verification.

## 5. Ask if Uncertain

If you're unsure about intent behind a change or user-facing impact, **ask the user** - don't guess.
