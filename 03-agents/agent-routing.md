# Agent Routing — Routing Table

> The vault is the single source of truth. Before any task — check which agent to invoke.

---

## Trigger Matrix (When to Activate — Exact Triggers)

**Decision rule:** Scan user message + task. If ANY trigger matches, invoke that agent. Use FIRST match (lowest priority number) when multiple apply. No match → default behavior.

| Priority | Trigger keywords/phrases | Agent | File |
|----------|--------------------------|-------|------|
| 1 | bug, error, crash, not working, broken, investigate, fix, debug | debugger | specialists/debugger |
| 2 | deploy, production, server, pm2, ssh, release, rollback, ci/cd | devops-engineer | specialists/devops-engineer |
| 3 | pentest, exploit, attack, hack, breach, pwn, redteam, offensive | penetration-tester | specialists/penetration-tester |
| 4 | security, vulnerability, owasp, xss, injection, encrypt, supply chain, security audit | security-auditor | specialists/security-auditor |
| 5 | mobile, react native, flutter, ios, android, app store, expo | mobile-developer | specialists/mobile-developer |
| 6 | database, sql, schema, migration, query, postgres, index, table | database-architect | specialists/database-architect |
| 7 | backend, server, api, endpoint, auth | backend-specialist | specialists/backend-specialist |
| 8 | component, react, vue, ui, ux, css, tailwind, responsive, frontend | frontend-specialist | specialists/frontend-specialist |
| 9 | test, spec, coverage, jest, pytest, playwright, e2e, unit test | test-engineer | specialists/test-engineer |
| 10 | performance, optimize, speed, slow, memory, cpu, benchmark, lighthouse | performance-optimizer | specialists/performance-optimizer |
| 11 | seo, meta, core web vitals, e-e-a-t, ai search visibility | seo-specialist | specialists/seo-specialist |
| 12 | readme, api docs, changelog, documentation (explicit request) | documentation-writer | specialists/documentation-writer |
| 13 | codebase, discovery, audit, refactor plan, map structure | explorer-agent | specialists/explorer-agent |
| 14 | healthcare, legitscript, fda, advertising platform compliance | compliance-auditor | specialists/compliance-auditor |
| 15 | gold ira, ira content, precious metals | gold-ira-seo-content-writer | content/gold-ira-seo-content-writer |
| 16 | architecture, stack, tech decisions, cto | cto | core/cto |
| 17 | plan, breakdown, tasks, project planning, PLAN.md | project-planner | core/project-planner |
| 18 | execution plan, 🟩🟨🟥, create plan | create-plan | core/create-plan |
| 19 | orchestrate, multi-agent, 3+ agents, coordination | orchestrator | core/orchestrator |
| 20 | brainstorm, explore options, design exploration | brainstorm | workflows/brainstorm |
| 21 | /document, update docs, documentation (post-execution) | document | workflows/document |
| 22 | /execute, implement plan | execute | workflows/execute |
| 23 | /debug | debug | workflows/debug |
| 24 | /deploy, production release | deploy | workflows/deploy |
| 25 | /review, code review | review | workflows/review |
| 26 | /create, new app | create | workflows/create |
| 27 | /plan | plan | workflows/plan |
| 28 | /test, run tests | test | workflows/test |
| 29 | /status, progress | status | workflows/status |
| 30 | /preview, dev server | preview | workflows/preview |
| 31 | /enhance, add feature | enhance | workflows/enhance |
| 32 | ui/ux pro, design system | ui-ux-pro-max | workflows/ui-ux-pro-max |
| 33 | peer review | peer-review | workflows/peer-review |
| 34 | learning, teach, explain | learning-opportunity | workflows/learning-opportunity |
| 35 | compliance scan (healthcare) | compliance | workflows/compliance |

---

## Core

| Task | Agent | Location | Notes |
|------|-------|----------|-------|
| Multi-agent coordination | orchestrator | core/ | min 3 agents |
| Task planning, PLAN.md | project-planner | core/ | before orchestration |
| Execution plan (🟩🟨🟥) | create-plan | core/ | |
| Architecture, CTO | cto | core/ | Read project brief from 02-projects for stack |

## Specialists

| Task | Agent | Location |
|------|-------|----------|
| React, UI, components | frontend-specialist | specialists/ |
| API, backend, Firebase | backend-specialist | specialists/ |
| Security, OWASP | security-auditor | specialists/ |
| Unit, E2E, coverage | test-engineer | specialists/ |
| Bugs, root cause | debugger | specialists/ |
| SEO, meta, analytics | seo-specialist | specialists/ |
| Schema, migrations | database-architect | specialists/ |
| CI/CD, deploy | devops-engineer | specialists/ |
| React Native, Flutter | mobile-developer | specialists/ |
| Profiling, optimization | performance-optimizer | specialists/ |
| Red team, pentest | penetration-tester | specialists/ |
| Compliance, regulation | compliance-auditor | specialists/ |
| Codebase discovery | explorer-agent | specialists/ |
| Docs, README | documentation-writer | specialists/ |

## Content

| Task | Agent | Location |
|------|-------|----------|
| Gold IRA content, E-E-A-T, GEO | gold-ira-seo-content-writer | content/ |

## Workflows

| Task | Workflow | Location |
|------|----------|----------|
| Structured coordination | orchestrate | workflows/ |
| Exploration, design | brainstorm | workflows/ |
| Planning | plan | workflows/ |
| Feature creation | create | workflows/ |
| Debug | debug | workflows/ |
| Deploy | deploy | workflows/ |
| Documentation | document | workflows/ |
| Execution | execute | workflows/ |
| Code review | review | workflows/ |
| Peer review | peer-review | workflows/ |
| Learning opportunity | learning-opportunity | workflows/ |
| UI/UX pro | ui-ux-pro-max | workflows/ |
| Test | test | workflows/ |
| Status | status | workflows/ |
| Preview | preview | workflows/ |
| Enhance | enhance | workflows/ |
| Compliance | compliance | workflows/ |

## Common Flows

| Scenario | Order |
|----------|-------|
| New feature | project-planner → create-plan → frontend/backend → test-engineer |
| Bug | debugger → test-engineer (regression) |
| Security review | security-auditor → (optional) penetration-tester |
| Gold IRA content | gold-ira-seo-content-writer |
| Architecture | cto / project-planner |
| Deploy | devops-engineer → deploy workflow |
