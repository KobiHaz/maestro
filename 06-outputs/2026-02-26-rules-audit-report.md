# Rules Audit for All Projects — 2026-02-26

> Systematic check: which files should be rules for all projects, and whether they are correctly connected/activated.

---

## 1. Rules File Map (per CLAUDE.md)

According to `CLAUDE.md`, the following files should be read before tasks:

| Task Type | File | Path | Status |
|-----------|------|------|--------|
| **Every task** | CLAUDE.md | vault root | ✅ always_applied (Cursor) |
| **Every task** | 01-me | 01-me/* | ⚠️ manual read required |
| **Writing** | 01-me-writing | 01-me/01-me-writing.md | ⚠️ manual read required |
| **Project work** | Project brief | 02-projects/[project]/ | ⚠️ manual read required |
| **Working with agents** | agent-routing | 03-agents/agent-routing.md | ⚠️ manual read required |
| **Specific agent** | Agent files | 03-agents/core/, specialists/, content/, workflows/ | Depends on choice |

---

## 2. How Are Rules Connected in Practice?

### 2.1 Current Workspace (Maestro Vault)

- **Cursor** — workspace is the vault itself.
- **CLAUDE.md** — defined as `always_applied_workspace_rules` so it is **loaded automatically**.
- Other files (01-me, agent-routing, etc.) are **not** loaded automatically — CLAUDE instructs the AI to read them before tasks, but there is no technical enforcement.

### 2.2 External Projects (hadaryaCRM, CMS, etc.)

Per `03-agents/README.md` and `docs/plans/2026-02-26-vault-improvement.md`:

- Model: `maestro/01-me` and `maestro/03-agents` = **symlink** to vault folders.
- **Not verified** — no clear location for projects (`02-projects/README` mentions `~/.gemini/antigravity/projects/` — different path from the plan).
- **Potential issue** — when opening Cursor in a project folder (not the vault), there may not be access to CLAUDE.md or 01-me unless there is a symlink **and the project is configured to use it**.

### 2.3 Gaps

- No `.cursorrules` or `.cursor/rules/` in the vault.
- No `AGENTS.md`.
- Rules rely on:
  1. `CLAUDE.md` (always_applied only when workspace is the vault)
  2. Text instructions to read specific files before tasks

---

## 3. Agents (03-agents) — Alignment with agent-routing

### 3.1 Core Agents

| Agent | File | Frontmatter (name+description) | In agent-routing |
|-------|------|-------------------------------|------------------|
| orchestrator | core/orchestrator.md | ✅ | ✅ |
| project-planner | core/project-planner.md | ✅ | ✅ |
| create-plan | core/create-plan.md | ✅ | ✅ |
| cto | core/cto.md | ✅ | ✅ |

### 3.2 Specialists

| Agent | File | Frontmatter | In agent-routing |
|-------|------|-------------|------------------|
| frontend-specialist | specialists/frontend-specialist.md | ✅ | ✅ |
| backend-specialist | specialists/backend-specialist.md | ✅ | ✅ |
| security-auditor | specialists/security-auditor.md | ✅ | ✅ |
| test-engineer | specialists/test-engineer.md | ✅ | ✅ |
| seo-specialist | specialists/seo-specialist.md | ✅ | ✅ |
| penetration-tester | specialists/penetration-tester.md | ✅ | ✅ |
| mobile-developer | specialists/mobile-developer.md | ✅ | ✅ |
| performance-optimizer | specialists/performance-optimizer.md | ✅ | ✅ |
| debugger | specialists/debugger.md | ✅ | ✅ |
| database-architect | specialists/database-architect.md | ✅ | ✅ |
| devops-engineer | specialists/devops-engineer.md | ✅ | ✅ |
| explorer-agent | specialists/explorer-agent.md | ✅ | ✅ |
| documentation-writer | specialists/documentation-writer.md | ✅ | ✅ |
| compliance-auditor | specialists/compliance-auditor.md | ✅ | ✅ |

### 3.3 Content

| Agent | File | Frontmatter | In agent-routing |
|-------|------|-------------|------------------|
| gold-ira-seo-content-writer | content/gold-ira-seo-content-writer.md | ✅ | ✅ |

### 3.4 Workflows

**All workflows lack `name` in frontmatter** (only `description` exists):

| Workflow | File | name | description | In agent-routing |
|----------|------|------|-------------|------------------|
| orchestrate | workflows/orchestrate.md | ❌ | ✅ | ✅ |
| brainstorm | workflows/brainstorm.md | ❌ | ✅ | ✅ |
| plan | workflows/plan.md | ❌ | ✅ | ✅ |
| create | workflows/create.md | ❌ | ✅ | ✅ |
| debug | workflows/debug.md | ❌ | ✅ | ✅ |
| deploy | workflows/deploy.md | ❌ | ✅ | ✅ |
| document | workflows/document.md | ❌ | ✅ | ✅ |
| execute | workflows/execute.md | ❌ | ✅ | ✅ |
| review | workflows/review.md | ❌ | ✅ | ✅ |
| peer-review | workflows/peer-review.md | ❌ | ✅ | ✅ |
| learning-opportunity | workflows/learning-opportunity.md | ❌ | ✅ | ✅ |
| ui-ux-pro-max | workflows/ui-ux-pro-max.md | ❌ | ✅ | ✅ |
| test | workflows/test.md | ❌ | ✅ | ✅ |
| status | workflows/status.md | ❌ | ✅ | ✅ |
| preview | workflows/preview.md | ❌ | ✅ | ✅ |
| enhance | workflows/enhance.md | ❌ | ✅ | ✅ |
| compliance | workflows/compliance.md | ❌ | ✅ | ✅ |

**Full alignment** — all files in agent-routing exist, and vice versa.

---

## 4. Textual Content (orchestrate.md)

- **Turkish text** — not present. Already fixed to `Approve plan? (Y/N)` ✅

---

## 5. Folder Structure and Role as Rules

| Folder | README | Role as rule |
|--------|--------|--------------|
| 00-inbox | ✅ | Capture and processing instructions |
| 01-me | ✅ (01-me-README) | Identity, writing, tools, AI preferences |
| 02-projects | ✅ | project briefs — rules per project |
| 03-agents | ✅ | routing + agents |
| 04-knowledge | ✅ | Check before new research |
| 05-templates | No | Format templates |
| 06-outputs | ✅ | naming convention |
| 07-logs | ✅ | Weekly documentation |

---

## 6. Project-Specific Content (Not General)

Deep check: texts tailored to specific project/company/technology instead of being general.

### 6.1 CTO Agent — **Fully specific to project leadslords**

| Line / Area | Specific content | Should be |
|-------------|------------------|------------|
| Lines 11–23 | "leadslords", React 19, Firebase (Firestore, Functions, Hosting), Vite, Tailwind v3, Framer Motion, TanStack Query, `@cms/shared`, ImageKit, Vitest, Playwright, Sentry, Firebase Analytics | Reference to `maestro.config.json` or project brief — not hardcode |
| Line 33 | "We use Firestore, so translate to Firestore/NoSQL" | General: "Use project's database. Check project brief for stack." |

**Conclusion:** cto.md = **profile of leadslords/CMS**, not a general CTO agent. Not suitable as a rule for all projects.

---

### 6.2 Gold IRA Content Agent — **Domain (niche) specific — not project**

| Line / Area | Content | Note |
|-------------|---------|------|
| Overall | Gold IRA, E-E-A-T, GEO, J.P. Morgan, IRS Section 408(m), precious metals | Agent for **niche** — Gold IRA only |
| agent-routing | "Gold IRA content, E-E-A-T, GEO" | Correct — explicitly defined for this niche |

**Conclusion:** Domain-specific (Gold IRA), not a single project. Matches agent-routing. **No issue** — intentionally niche agent.

---

### 6.3 `.agent/` Structure — **Antigravity-specific**

The following files assume Antigravity/Gemini agent folder structure:

| File | Reference | Issue |
|------|-----------|-------|
| orchestrator.md | `ARCHITECTURE.md`, `playwright_runner.py`, `security_scan.py` | Projects without `.agent/` won't find them |
| orchestrate.md | `python .agent/skills/.../security_scan.py`, `lint_runner.py`, `docs/PLAN.md` | Fixed paths |
| project-planner.md | `CODEBASE.md`, `python .agent/scripts/verify_all.py`, `playwright_runner.py`, `ux_audit.py`, `lighthouse_audit.py` | Depends on .agent |
| preview.md | `auto_preview.py` inside `.agent/scripts/` | Specific to projects with .agent |
| status.md | `session_manager.py`, `auto_preview.py` | Same |
| enhance.md | `session_manager.py` | Same |
| create.md | `auto_preview.py` | Same |
| compliance.md | `python .agent/skills/compliance-audit/scripts/compliance_checker.py` | Same |
| ui-ux-pro-max.md | `python3 .shared/ui-ux-pro-max/scripts/search.py` | Depends on `.shared/` (CMS structure?) |
| document.md | `CODEBASE.md` | Specific file name |

**Conclusion:** Many workflows are tailored to **Antigravity** structure (`.agent/`, `.shared/`). "Regular" projects (e.g. Cursor + Git only) won't use them.

---

### 6.4 01-me — **Intentionally personal/business**

| File | Specific content | Note |
|------|-----------------|------|
| 01-me-identity.md | hadaryaCRM, Xsheva, Quote systems, Stock bot, Affiliate, CMS | **Correct** — user's business identity |
| 01-me-tools.md | "hadaryaCRM & similar projects", Supabase, Firebase, Vercel | **Correct** — general tech preferences |
| 01-me-README | "business (Xsheva)" | **Correct** — business context |

**Conclusion:** 01-me **should** be specific — it's identity context. **No issue**.

---

### 6.5 02-projects — **Should be project-specific**

Every project brief there is project-specific. **No issue** — that's the purpose.

---

### 6.6 Texts in Other Languages (Examples)

| File | Line | Content |
|------|------|---------|
| orchestrate.md | 162–166 | CONTEXT example with "Öğrenciler için sosyal platform" (Turkish) — generic example, not critical |
| ui-ux-pro-max.md | 112–113 | "Làm landing page cho dịch vụ chăm sóc da" (Vietnamese) — example only |

**Conclusion:** Examples only, do not affect logic. Can be replaced with English for consistency if desired.

---

### 6.7 Mismatches Between orchestrator and agent-routing

| Agent | orchestrator.md (line 99) | agent-routing.md | Status |
|-------|----------------------------|------------------|--------|
| api-designer | Listed | ❌ not present | orchestrator references agent not in routing |

---

## 7. Project-Specific Content Summary

| Type | Examples | Severity | Recommendation |
|------|----------|----------|----------------|
| **CTO Agent** | leadslords, Firebase, @cms/shared, ImageKit | 🔴 High | Turn into template; stack from project brief / maestro.config |
| **.agent/ structure** | security_scan.py, playwright_runner, auto_preview | 🟡 Medium | Add "If project has .agent/…" or separate workflow for projects with/without .agent |
| **ui-ux-pro-max** | .shared/ui-ux-pro-max/scripts | 🟡 Medium | State that it's for projects with .shared structure |
| **Gold IRA** | Domain agent | ✅ OK | Intended for niche — no change |
| **01-me** | Xsheva, hadaryaCRM | ✅ OK | Identity context — no change |
| **api-designer** | orchestrator refers | 🟡 Low | Remove from orchestrator list or create the agent |

---

## 8. Summary and Recommendations (Update)

### ✅ What Works

1. **CLAUDE.md** — loaded automatically in Cursor when working in the vault.
2. **Agents** — Core + Specialists + Content with full frontmatter.
3. **agent-routing** — 100% aligned with file list.
4. **Folder structure** — README and clear documentation.
5. **VAULT_PATH.md** — exists and defined.

### ⚠️ Issues

1. **01-me, agent-routing, project briefs** — no automatic enforcement; AI must follow CLAUDE instructions.
2. **Workflows** — missing `name` in frontmatter (Task 2.3 in improvement plan).
3. **External projects** — symlink connection not verified; project paths (`~/.gemini/antigravity/`) don't match plan (hadaryaCRM, CMS).
4. **Project-specific content** — cto.md = leadslords profile; many workflows depend on `.agent/` (Antigravity); ui-ux-pro-max on `.shared/`.

### Action Recommendations

| # | Action | Priority |
|---|--------|----------|
| 1 | **cto.md** — Separate: general template vs leadslords profile (or move to 02-projects/leadslords/) | 🔴 High |
| 2 | **Workflows with .agent/** — Add "if .agent/ exists" condition or separate workflow for projects without Antigravity | 🟡 Medium |
| 3 | **ui-ux-pro-max** — Explicitly state dependency on `.shared/` | 🟡 Medium |
| 4 | **orchestrator** — Remove `api-designer` or create the agent | Low |
| 5 | Add `name` to 17 workflows in frontmatter | Low (consistency) |
| 6 | Verify symlinks: hadaryaCRM, CMS → 01-me, 03-agents | Medium |
| 7 | Update 02-projects/README with current project paths | Low |
| 8 | Consider adding `.cursorrules` or rules in `.cursor/rules/` that reference 01-me and agent-routing | Optional |

---

## 9. Execution Plan

Plan: [[docs/plans/2026-02-26-vault-rules-generalization]]
Status: [x] Layer 1 (CTO) | [x] Layer 2 (.agent/) | [x] Layer 3 (frontmatter) | [x] Layer 4 (verification)

---

*Created: 2026-02-26 | Updated: Deep check for project-specific content | Executed: 2026-02-26*
