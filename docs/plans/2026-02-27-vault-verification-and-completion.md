# Vault Verification & Completion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify every item from prior plans (vault-improvement, vault-rules-generalization), document findings, and complete any remaining gaps.

**Architecture:** Verification-first. Each task: (1) Verify current state, (2) Document result, (3) Remediate only if missing. No assumptions—grep/ls/read to confirm.

**Tech Stack:** Markdown, YAML frontmatter, bash verification commands.

---

## Pre-Plan Verification (2026-02-27)

| Item | Source Plan | Verified | Result |
|------|-------------|----------|--------|
| VAULT_PATH.md | vault-improvement 1.1 | ✅ | Exists |
| Home.md | vault-improvement 3.2 | ✅ | Exists |
| AGENT-TEMPLATE.md | vault-improvement 2.1 | ✅ | Exists |
| orchestrate.md Turkish | vault-improvement 2.2 | ✅ | Fixed ("Approve plan? (Y/N)") |
| Workflow `name` (17) | vault-rules-generalization 3.1 | ✅ | All 17 have `name:` |
| cto.md generalized | vault-rules-generalization 1.2 | ✅ | No leadslords; "project brief" present |
| api-designer removed | vault-rules-generalization 3.2 | ✅ | 0 matches |
| 00-inbox README | vault-improvement 4.1 | ✅ | Exists (+ project sections) |
| 04-knowledge README | vault-improvement 4.2 | ✅ | Exists |
| 05-templates | vault-improvement 4.3 | ✅ | project-brief, output-post, meeting-notes |
| 06-outputs README | vault-improvement 4.4 | ✅ | Exists |
| 07-logs README + W09 | vault-improvement 4.5 | ✅ | Exists |
| 02-projects | PKM + summary | ✅ | 6 projects with briefs |
| cto-leadslords profile | vault-rules-generalization 1.1 | ⊘ | SKIPPED — not needed |
| Symlinks (hadaryaCRM, cms) | vault-improvement 1.2–1.3 | ⊘ | N/A — vault is workspace, not projects |
| 01-me/system | PKM analysis | ❌ | Not created |
| .agent/ Prerequisites | vault-rules-generalization Layer 2 | ✅ | Obsolete — no .agent/. Maestro vault is the infrastructure. Workflows updated. |

---

## Decisions (2026-02-27)

| Decision | Rationale |
|----------|-----------|
| **Symlinks in projects** | Vault (Obsidian) is the Cursor workspace. 01-me, 03-agents, CLAUDE.md already loaded. No need for maestro/ inside project folders. |
| **cto-leadslords profile** | Not needed. cto.md is generalized; project briefs suffice. |

---

## Layer 1: .agent/ Prerequisites Audit → OBSOLETE

**Status (2026-02-27):** No .agent/ folder. Maestro vault is the agent infrastructure. Workflows updated to use project-standard commands (`npm run lint`, `npm run build`, `npm run dev`). Task 1.1 skipped — not applicable.

---

## Layer 2: 01-me/system (PKM Recommendation)

### Task 2.1: Create 01-me/system structure

**Purpose:** PKM analysis recommended a place for principles, routines, meta.

**Files:**
- Create: `01-me/system/README.md`
- Create: `01-me/system/principles.md`
- Create: `01-me/system/routines.md`

**01-me/system/README.md:**

```markdown
# System / Meta

Working principles and routines. Read before complex tasks if relevant.
```

**01-me/system/principles.md:**

```markdown
---
---

# Principles

- Inbox first — capture in 00-inbox before processing
- Agent per task — route via agent-routing
- Verify before completion — run checks before claiming done
```

**01-me/system/routines.md:**

```markdown
---
---

# Routines

- **Weekly:** Process inbox, update 07-logs
- **Before project work:** Read project brief from 02-projects
```

**Step 2: Update CLAUDE.md**

**Files:**
- Modify: `CLAUDE.md`

**Action:** In "Agent Protocol" section, add: "Before complex tasks — read 01-me/system/principles if relevant."

**Verification:** `ls 01-me/system/` shows 3 files. CLAUDE.md mentions system.

---

## Layer 3: Final Verification Checklist

### Task 3.1: Run full verification script

**Create verification script (optional, for repeatability):**

**Files:**
- Create: `docs/scripts/verify-vault.sh` (optional)

**Content:**

```bash
#!/usr/bin/env bash
set -e
VAULT="${1:-.}"
echo "=== Vault Verification ==="
echo "VAULT_PATH.md: $(test -f $VAULT/VAULT_PATH.md && echo OK || echo MISSING)"
echo "Home.md: $(test -f $VAULT/Home.md && echo OK || echo MISSING)"
echo "AGENT-TEMPLATE: $(test -f $VAULT/03-agents/AGENT-TEMPLATE.md && echo OK || echo MISSING)"
echo "Workflow names: $(grep -c '^name:' $VAULT/03-agents/workflows/*.md 2>/dev/null | grep -c 1 || echo 0) (expect 17)"
echo "cto leadslords: $(grep -c leadslords $VAULT/03-agents/core/cto.md 2>/dev/null || echo 0) (expect 0)"
echo "api-designer: $(grep -rlc api-designer $VAULT/03-agents/ 2>/dev/null | wc -l) (expect 0)"
echo "02-projects: $(ls -1 $VAULT/02-projects/*/project.*.md 2>/dev/null | wc -l) briefs"
echo "01-me/system: $(test -d $VAULT/01-me/system && echo OK || echo MISSING)"
```

**Verification:** Run from vault root; all checks pass or documented.

---

### Task 3.2: Update summary report

**Files:**
- Modify: `06-outputs/2026-02-27-summary-report-outputs-and-plans.md`

**Action:** Add section "Post-Verification Update (2026-02-27)" with:
- Verification plan executed
- Gaps found and fixed
- Decisions: symlinks N/A (vault=workspace), cto-leadslords skipped
- 01-me/system created

**Verification:** Summary report reflects completion state.

---

## Verification Checklist (Final)

After all tasks:

- [x] Task 1.1: N/A — no .agent/; workflows updated
- [ ] Task 2.1: 01-me/system created, CLAUDE.md updated
- [ ] Task 3.1: Verification script run (optional)
- [ ] Task 3.2: Summary report updated

---

*Plan created: 2026-02-27 | Updated: 2026-02-27 — symlinks N/A, cto-leadslords skipped*
