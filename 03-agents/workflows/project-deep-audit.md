---
name: project-deep-audit
description: Comprehensive project research and audit. Uses ALL relevant agents, 04-knowledge, 02-projects brief, and skills. Trigger: deep research, full review (Hebrew variants also), comprehensive audit, full project review, activate all agents.
---

# Project Deep Audit — deep research and full review

When the user requests **comprehensive research**, **full audit**, or **activation of all agents and knowledge** for a development project — use this workflow.

## Purpose

Ensure **nothing is left unused**:
- **02-projects/** — Project brief (stack, status, decisions)
- **04-knowledge/** — Reference docs, architecture, standards, prior audits
- **03-agents/specialists/** — Domain experts per project type
- **03-agents/skills/** — Scripts (audit, security, UX, etc.)
- **Output** → `06-outputs/YYYY-MM-DD-<project>-audit-report.md`

---

## Mandatory Pre-Flight (Before ANY agent)

### Step 1: Identify Project

| Source | Action |
|-------|--------|
| User named project | Use that project |
| User in project folder / file | Infer from path (e.g. `source6681`) |
| Unclear | Ask: "Which project should I audit? (02-projects lists available)" |

**Project list:** `Glob 02-projects/*/project.*.md`

### Step 2: Load Vault Context (MANDATORY)

**Always read before invoking any agent:**

```
1. 02-projects/<project>/project.<project>.md     ← Stack, path, type, agents
2. 04-knowledge/reference/<project>-*.md         ← Architecture, prior audits
3. 04-knowledge/standards/<project>-standards.md
4. 02-projects/<project>/plans-and-tasks.md     ← Current state
```

**If no 04-knowledge docs exist** — Note that. Still proceed. Output will recommend creating them.

### Step 3: Map Project Type → Agents & Scripts

| Project Type | Agents to invoke | Scripts to run (if present) |
|--------------|------------------|----------------------------|
| WEB | frontend-specialist, backend-specialist, security-auditor, test-engineer, performance-optimizer, seo-specialist, database-architect, devops-engineer, documentation-writer | ux_audit.py, security_scan.py, lighthouse_audit.py, seo_checker.py |
| MOBILE | mobile-developer, security-auditor, test-engineer, performance-optimizer | mobile_audit.py |
| BACKEND | backend-specialist, database-architect, security-auditor, test-engineer, devops-engineer, documentation-writer | security_scan.py, lint_runner.py |

**Plus always:** explorer-agent (discovery first), **cto** (**CTO persona** section in `workflows/brainstorm.md` — architecture review), **`workflows/plan.md`** / `project-planner` (if gaps in plan).

**Conditional:** penetration-tester (when security is critical), compliance-auditor (healthcare, regulated industries).

---

## Audit Flow (Sequential)

### Phase 1: Discovery (explorer-agent)

1. Invoke **explorer-agent** with project path from brief
2. Scope: Architecture mapping, dependency tree, risk areas
3. Output: Structured findings (audit mode, not implementation)

### Phase 2: Domain Analysis (3+ specialists in parallel or sequence)

Invoke specialists based on project type. Pass full context:
- Project brief
- 04-knowledge docs
- Explorer findings
- Original user request

| Domain | Agent | Focus |
|--------|-------|-------|
| Discovery | explorer-agent | Architecture mapping, risk areas |
| Architecture | cto (`workflows/brainstorm.md` → CTO persona) | Stack, tech decisions, patterns |
| Security | security-auditor | Auth, vulns, supply chain |
| Backend | backend-specialist | API, logic, patterns |
| Frontend | frontend-specialist | UI, perf, a11y |
| DB | database-architect | Schema, migrations, indexes |
| Tests | test-engineer | Coverage, gaps |
| Ops | devops-engineer | CI/CD, deploy readiness |
| Perf | performance-optimizer | Bottlenecks, Lighthouse |
| SEO | seo-specialist | Meta, Core Web Vitals, AI search visibility |
| Docs | documentation-writer | README, API docs, changelog clarity |

### Phase 3: Script Execution (when applicable)

Run audit scripts from `03-agents/skills/`:

```bash
# Security (if Node/JS project)
python 03-agents/skills/vulnerability-scanner/scripts/security_scan.py <project_path>

# UX (web)
python 03-agents/skills/frontend-design/scripts/ux_audit.py <project_path>

# Lighthouse (if URL available)
python 03-agents/skills/performance-profiling/scripts/lighthouse_audit.py <url>

# Mobile
python 03-agents/skills/mobile-design/scripts/mobile_audit.py <project_path>
```

### Phase 4: Synthesis Report

Create `06-outputs/YYYY-MM-DD-<project>-audit-report.md`:

```markdown
# Project Audit Report — [project]

**Date:** YYYY-MM-DD  
**Project:** [name]  
**Type:** WEB/MOBILE/BACKEND

## Sources Used
- 02-projects/[project]/project.[project].md
- 04-knowledge/reference/[project]-*
- Agents: explorer-agent, [list specialists]
- Scripts: [list run]

## Findings by Domain
### Discovery (explorer-agent)
### Architecture (cto — `workflows/brainstorm.md`, CTO persona section)
### Security (security-auditor)
### Backend (backend-specialist)
### Frontend (frontend-specialist)
### Database (database-architect)
### Tests (test-engineer)
### Ops (devops-engineer)
### Performance (performance-optimizer)
### SEO (seo-specialist)
### Documentation (documentation-writer)
...

## Recommendations (Prioritized)
1. P0 — Critical
2. P1 — High
3. P2 — Medium

## Knowledge Gaps
- [ ] Create/update 04-knowledge/reference/[project]-architecture.md
- [ ] Create/update 04-knowledge/standards/[project]-standards.md

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

---

## Integration with Agent Routing

This workflow is triggered by (add to agent-routing Trigger Matrix):
- comprehensive audit, full project review, deep research, activate all agents
- Hebrew phrases for the same intent (e.g. deep research, full review, run all agents)
- project audit, deep research [project]
- “all agents on [project]” style requests

**Priority:** High (e.g. 5) — before single-domain specialists.

---

## Exit Gate

Before marking audit complete:

- [ ] Project brief loaded
- [ ] 04-knowledge checked (used if exists)
- [ ] explorer-agent invoked
- [ ] ≥3 specialists invoked (or all relevant for project type)
- [ ] ≥1 script run (when applicable)
- [ ] Report saved to 06-outputs with date

> **Workspace = Vault.** Project code may live externally. Always use project brief path for scripts and agent context.
