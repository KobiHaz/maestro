# Agent Routing — catalog aligned to file contents

> **Source of truth for folder split** is what is written *inside* each file under `03-agents/`, not a legacy table. This document records that split and the **workflow lifecycle order**.

The vault is the single source of truth. **Planned work** is staffed from the catalog below + **`workflows/plan.md`** (staffing alias **`project-planner`**); keyword hints are optional for ad-hoc chat only.

---

## Supply cycle — catalog alignment (no separate meta doc)

**Principle:** No single file describes the whole process end-to-end. **Every** workflow under `workflows/` and persona under `specialists/` defines **inside itself** (section **Place in the supply cycle**) which stage it is, what usually comes before and after. **`core/`** is optional for future persistent personas (see `core/README.md`).  
**This document** complements that in two ways: (a) **alignment table** — which stages exist and the main “owners” per stage; (b) **staffing** — which specialist and which workflow fit which kind of work, so **`workflows/plan.md`** (alias `project-planner`) can write real paths under `03-agents/`.

| Stage | What happens here | Main implementation (files) |
|-------|-------------------|------------------------------|
| **1 — Specification** | Pain, goals, requirements, direction | `workflows/brainstorm.md` (**`/brainstorm`** + **CTO persona** in the same file) + **PRD** (PRD section in `workflows/plan.md`, or **`/prd`**) + specialists from the tables below as needed |
| **2 — Planning** | Break into tasks, dependencies, **staffing**, 🟩🟨🟥 | **`workflows/plan.md`** only (`/plan` + `/prd` in one file; reads **tables in this document** and writes `03-agents/...` per task in `docs/plans/{slug}.md`) |
| **3 — Execution** | Implement per plan | `workflows/execute.md`; greenfield: `workflows/create.md` when appropriate |
| **4 — Testing** | Verification, coverage, regressions | Required inside `execute`; extend: `workflows/test.md` + `test-engineer` |
| **5 — Documentation** | Docs consistent with implementation | `workflows/document.md` + `documentation-writer` |
| **6 — Quality & close-out** | Code review, branch wrap-up | `workflows/review.md`, `workflows/finishing-branch.md` |

**Staffing:** From project spec and task — pick from `specialists/` and `workflows/` **using the catalog here**. Do not guess names that are not in the tables.  
**Multi-agent coordination:** **Orchestrator persona** in this file (`agent-routing.md`) + `workflows/orchestrate.md` — when 3+ perspectives are needed **per the plan**; does not replace the catalog or `/execute` when work is task-driven from the plan.

**Default order for a feature:** brainstorm → (optional CTO from `brainstorm`) → **PRD** in **`workflows/plan.md`** (`/prd`) → **`/plan`** → `/execute` (tests before claiming “done”) → `/test` as needed → `/document` → `/review` → `/finishing-branch`.

---

## How to decide: core / specialists / workflows

| Folder | By file content | Example |
|--------|-----------------|---------|
| **`core/`** | Reserved for **persistent personas** (“You are…” style) if you add them; may be empty. **Planning + PRD** live in `workflows/plan.md`. **Multi-agent coordination** is embedded in **this document** (Orchestrator persona). **CTO** lives in `workflows/brainstorm.md`. | See `core/README.md` |
| **`specialists/`** | **Domain expert** (security, frontend, DB, testing, …) — narrow technical persona. | `debugger`, `frontend-specialist`, … |
| **`workflows/`** | **Process / mode**: steps, checklist, `/execute` wiring, or wrapper that routes to another agent. | `execute`, `brainstorm`, `plan`, … |

**Rules:**

- **Single planning path:** **`workflows/plan.md`** (`/plan`, `/prd`) → `docs/plans/{slug}.md` (staffing, tasks, **Overall Progress**, **🟩🟨🟥**).
- **`workflows/compliance.md`** invokes **`specialists/compliance-auditor.md`** (process vs persona).

---

## Routing model (catalog first, not keywords)

| Layer | When | What to do |
|-------|------|------------|
| **1 — Catalog + plan** | There is (or you will create) `docs/plans/{slug}.md` / **`workflows/plan.md`** | **`project-planner`** (this file = `03-agents/workflows/plan.md`) picks agents from the tables below + files under `03-agents/`. Staffing in the plan is source of truth — **do not** guess from keywords. |
| **2 — Explicit call** | User says `/execute`, `frontend-specialist`, `workflows/review.md`, etc. | Run what was named — priority over guessing. |
| **3 — Quick hint (optional)** | Free chat **without** an open plan and without an explicit command | **Trigger Matrix** suggests a first workflow/agent — suggestion only. |

**Rule:** Staffing in `docs/plans/*.md` **overrides** any keyword match. For several agents, use `workflows/orchestrate.md` + **Orchestrator persona** in this document — coordinate; do not replace specialists.

## Flow: agent staffing (`workflows/plan.md` — alias `project-planner`)

**`project-planner`** (alias for **`/plan`** — file `03-agents/workflows/plan.md`): every plan must staff a concrete **vault path** per task: `03-agents/specialists/…` or `03-agents/workflows/…` (and `03-agents/core/…` only if a core persona exists), consistent with **this file**. If nothing fits — **New agent checklist** + [[AGENT-TEMPLATE]].

**Required in plan:** task → **name** + **`03-agents/...` path**.

**Execution:** `/execute` reads staffing from the plan — no invented names.

## Project rules (required for every project)

1. **Single source** — `02-projects/<project>/plans-and-tasks.md`
2. **Delete after done** — sync then remove ephemeral `docs/plans/*` per lifecycle doc
3. **Update documentation** — `04-knowledge/` as needed

Details: [[04-knowledge/standards/maestro-project-doc-lifecycle]]

---

## Trigger Matrix (optional — free chat without a plan)

**When:** no relevant `docs/plans/*.md` open and the user did not name a workflow/agent explicitly.

**Decision rule:** FIRST match (lowest priority number). Hebrew variants noted inline where useful for matching.

| Priority | Trigger keywords/phrases | Invoke | File |
|----------|--------------------------|--------|------|
| 0 | new idea, new feature, add feature, change request, what if; Hebrew: רעיון חדש, פיצ'ר חדש, שינוי | brainstorm | workflows/brainstorm |
| 1 | prd, PRD, spec, specification, product requirements; Hebrew: איפיון, אפיון, דרישות מוצר | prd (section in workflows/plan) | workflows/plan → **PRD** |
| 2 | bug, error, crash, not working, broken, investigate, fix, debug | debugger | specialists/debugger |
| 3 | deploy, production, server, pm2, ssh, release, rollback, ci/cd | devops-engineer | specialists/devops-engineer |
| 4 | pentest, exploit, attack, hack, breach, pwn, redteam, offensive | penetration-tester | specialists/penetration-tester |
| 5 | security, vulnerability, owasp, xss, injection, encrypt, supply chain, security audit | security-auditor | specialists/security-auditor |
| 6 | comprehensive audit, full project review, project audit, activate all agents, deep research; Hebrew: מחקר מעמיק, סקירה מקיפה, הפעיל את הכל | project-deep-audit | workflows/project-deep-audit |
| 7 | mobile, react native, flutter, ios, android, app store, expo | mobile-developer | specialists/mobile-developer |
| 8 | database, sql, schema, migration, query, postgres, index, table | database-architect | specialists/database-architect |
| 9 | backend, server, api, endpoint, auth | backend-specialist | specialists/backend-specialist |
| 10 | component, react, vue, ui, ux, css, tailwind, responsive, frontend | frontend-specialist | specialists/frontend-specialist |
| 11 | test, spec, coverage, jest, pytest, playwright, e2e, unit test | test-engineer | specialists/test-engineer |
| 12 | performance, optimize, speed, slow, memory, cpu, benchmark, lighthouse | performance-optimizer | specialists/performance-optimizer |
| 13 | seo, meta, core web vitals, e-e-a-t, ai search visibility | seo-specialist | specialists/seo-specialist |
| 14 | readme, api docs, changelog, documentation (explicit request) | documentation-writer | specialists/documentation-writer |
| 15 | codebase, discovery, audit, refactor plan, map structure | explorer-agent | specialists/explorer-agent |
| 16 | healthcare, legitscript, fda, advertising platform compliance | compliance-auditor | specialists/compliance-auditor |
| 17 | gold ira, ira content, precious metals | gold-ira-seo-content-writer | content/gold-ira-seo-content-writer |
| 18 | architecture, stack, tech decisions, cto | cto (persona in brainstorm) | workflows/brainstorm → **CTO persona** |
| 19 | plan, /plan, breakdown, tasks, project planning, PLAN.md, execution plan, 🟩🟨🟥, create plan; Hebrew: תכנון, תוכנית עבודה | plan → project-planner | workflows/plan |
| 20 | orchestrate, multi-agent, 3+ agents, coordination | orchestrator | agent-routing (Orchestrator persona) |
| 21 | brainstorm, explore options, design exploration | brainstorm | workflows/brainstorm |
| 22 | /document, update docs, documentation (post-execution) | document | workflows/document |
| 23 | /execute, implement plan | execute | workflows/execute — **After completion:** plan-lifecycle checklist |
| 24 | /debug | debug | workflows/debug |
| 25 | /deploy, production release | deploy | workflows/deploy |
| 26 | /review, code review | review | workflows/review |
| 27 | /create, new app | create | workflows/create |
| 28 | /test, run tests | test | workflows/test |
| 29 | /status, /preview, progress, dev server, localhost | status | workflows/status — **includes start/stop/restart/check dev server (formerly `/preview`)** |
| 30 | /enhance, add feature | enhance | workflows/enhance |
| 31 | ui/ux pro, design system, design intelligence | ui-ux-specialist | specialists/ui-ux-specialist |
| 32 | peer review | peer-review | workflows/peer-review |
| 33 | learning, teach, explain; Hebrew: למד אותי | technical-educator | specialists/technical-educator |
| 34 | compliance scan (healthcare) | compliance | workflows/compliance |
| 35 | game, Unity, Godot, Phaser, Unreal, multiplayer, VR, AR | game-developer | games/game-developer |
| 36 | /finishing-branch, finish branch, merge branch, open PR, all done | finishing-branch | workflows/finishing-branch |
| 37 | jules, Jules scheduled task, Jules PR, fix/daily-scan, chore/standards | jules | specialists/jules |

**Brainstorm:** priorities **0** and **21** point to the same file; lower number wins.

**Skills index:** [[skills/README]]

### New agent checklist

1. Role, deliverables, verification note (use `04-knowledge/` / project brief as needed).
2. **New file placement by content:** **multi-agent orchestrator** → register in **tables in this document** (no separate `core/` file); **CTO** → `workflows/brainstorm.md`; planning + PRD → **`workflows/plan.md`**; domain expert → `specialists/` / `content/` / `games/`; slash workflow → `workflows/`. **Do not** add a second plan workflow — extend **`workflows/plan.md`** only.
3. Register in the matching table in **this file** (required for staffing via **`workflows/plan.md`**).
4. *(Optional)* Trigger Matrix row.
5. [[README]] if layout changes.

---

## Core (coordination & planning personas)

| Task | Agent | Path | Notes |
|------|-------|------|-------|
| Multi-agent coordination | orchestrator | `03-agents/agent-routing.md` (**Orchestrator persona** section) | min 3 agents; uses Agent tool |
| Task planning + staffing + 🟩🟨🟥; **PRD** (section in file) | plan / project-planner | `03-agents/workflows/plan.md` | **`/plan`**, **`/prd`** |
| **CTO (SOLUTIONING)** | cto | `03-agents/workflows/brainstorm.md` (**CTO persona** section) | `agent_path` to this file; separate from `workflows/plan.md` |

---

## Specialists (domain experts) — alphabetical

| Task | Agent | Path |
|------|-------|------|
| API, backend, Firebase | backend-specialist | `03-agents/specialists/backend-specialist.md` |
| Compliance, regulation | compliance-auditor | `03-agents/specialists/compliance-auditor.md` |
| Bugs, root cause | debugger | `03-agents/specialists/debugger.md` |
| Schema, migrations | database-architect | `03-agents/specialists/database-architect.md` |
| CI/CD, deploy | devops-engineer | `03-agents/specialists/devops-engineer.md` |
| Docs, README | documentation-writer | `03-agents/specialists/documentation-writer.md` |
| Codebase discovery | explorer-agent | `03-agents/specialists/explorer-agent.md` |
| React, UI, components | frontend-specialist | `03-agents/specialists/frontend-specialist.md` |
| Jules (CI, scheduled tasks) | jules | `03-agents/specialists/jules.md` |
| React Native, Flutter | mobile-developer | `03-agents/specialists/mobile-developer.md` |
| Red team, pentest | penetration-tester | `03-agents/specialists/penetration-tester.md` |
| Profiling, optimization | performance-optimizer | `03-agents/specialists/performance-optimizer.md` |
| Security, OWASP | security-auditor | `03-agents/specialists/security-auditor.md` |
| SEO, meta, analytics | seo-specialist | `03-agents/specialists/seo-specialist.md` |
| Teach / explain (PM-level depth) | technical-educator | `03-agents/specialists/technical-educator.md` |
| Unit, E2E, coverage | test-engineer | `03-agents/specialists/test-engineer.md` |
| UI/UX research, design systems, UX spec | ui-ux-specialist | `03-agents/specialists/ui-ux-specialist.md` |

---

## Workflows (processes) — lifecycle order

### Phase 1 — Discovery & specification

| Workflow | Path | What the file does |
|----------|------|--------------------|
| brainstorm (+ CTO) | `03-agents/workflows/brainstorm.md` | **`/brainstorm`** + **CTO persona**; **PRD** — PRD section in `workflows/plan.md` |
| plan | `03-agents/workflows/plan.md` | **`/plan`**, **`/prd`** — one file: PRD + staffed plan + **Overall Progress** + 🟩🟨🟥 on tasks |
| project-deep-audit | `03-agents/workflows/project-deep-audit.md` | Full project audit |

### Phase 2 — Multi-agent coordination

| Workflow | Path | What the file does |
|----------|------|--------------------|
| orchestrate | `03-agents/workflows/orchestrate.md` | Structured coordination across agents |

### Phase 3 — Build, run, environment

| Workflow | Path | What the file does |
|----------|------|--------------------|
| create | `03-agents/workflows/create.md` | `/create` — new application |
| execute | `03-agents/workflows/execute.md` | `/execute` — implement per plan |
| enhance | `03-agents/workflows/enhance.md` | Feature extension |
| debug | `03-agents/workflows/debug.md` | `/debug` |
| deploy | `03-agents/workflows/deploy.md` | `/deploy` |
| test | `03-agents/workflows/test.md` | `/test` |
| status | `03-agents/workflows/status.md` | `/status` + dev server commands (formerly `/preview`) |

### Phase 4 — Quality, docs, close-out

| Workflow | Path | What the file does |
|----------|------|--------------------|
| review | `03-agents/workflows/review.md` | `/review` — code review |
| peer-review | `03-agents/workflows/peer-review.md` | Synthesize feedback from another model |
| document | `03-agents/workflows/document.md` | `/document` after execution |
| compliance | `03-agents/workflows/compliance.md` | `/compliance` — route to `compliance-auditor` |
| finishing-branch | `03-agents/workflows/finishing-branch.md` | Branch close-out, PR, merge |

---

## Games (archive — optional)

| Task | Agent | Location |
|------|-------|----------|
| Game development | game-developer | [[games/game-developer]] |
| Index | — | [[games/README]] |

## Content

| Task | Agent | Location |
|------|-------|----------|
| Gold IRA content | gold-ira-seo-content-writer | `03-agents/content/` |

---

## Common flows

| Scenario | Order |
|----------|-------|
| **New feature** | brainstorm → PRD in **`workflows/plan.md`** (optional, `/prd`) → **`/plan`** (staffing + 🟩🟨🟥; SOLUTIONING: **cto** → `brainstorm`, WEB+UI: **ui-ux-specialist`) → `/execute` (tests required before done) → `/test` as needed → **`/document`** → **`/review`** → finishing-branch |
| **Complex feature** (3+ domains) | … → **`/plan`** → **orchestrator** (`agent-routing`, Orchestrator persona) → `/execute` → `/test` as needed → **`/document`** → **`/review`** → finishing-branch |
| **Simple feature** | brainstorm → (optional Mini-PRD in **`workflows/plan.md`** or `plans-and-tasks.md`) → **`/plan`** → `/execute` → `/test` as needed → **`/document`** → **`/review`** → finishing-branch |
| Full project audit | project-deep-audit → `06-outputs/` |
| Bug | debugger → test-engineer (regression) |
| Security | security-auditor → (optional) penetration-tester |
| Gold IRA content | gold-ira-seo-content-writer |
| Deploy | devops-engineer → **deploy** workflow |

> **Flow rule:** execute → **review** (required) → finishing-branch.

---

## Orchestrator persona (embedded in this document)

> **Activation:** When a plan task sets `agent`: `orchestrator`, `agent_path`: `03-agents/agent-routing.md` — operate as the persona below. **Tools:** Read, Grep, Glob, Bash, Write, Edit, Agent. **Skills:** clean-code, parallel-agents, behavioral-modes, plan-writing, brainstorming, architecture, lint-and-validate, powershell-windows, bash-linux.

You are the master orchestrator agent. You coordinate multiple specialized agents using Claude Code's native Agent Tool to solve complex tasks through parallel analysis and synthesis.

### Place in the supply cycle (Orchestrator)

- **Stage:** **Cross-domain coordination** — usually around **execution** or **pre-execution**, when 3+ distinct agents are needed in parallel.
- **Before:** Plan in `docs/plans/{slug}.md` (from **`workflows/plan.md`** / staffing alias `project-planner`) with staffing; without a plan — do not open with specialists (see checkpoints below).
- **After:** Synthesized outputs → continue **`/execute`**, or end the round per plan; does not replace **`/document`** / **`/review`**.
- **Staffing:** Agents you invoke must match **tables in this document** and the plan — not new roles outside the catalog.

### RUNTIME CAPABILITY CHECK (FIRST STEP)

**Before planning, verify project context:**
- [ ] **Read `ARCHITECTURE.md` or `CODEBASE.md`** if present; otherwise use README and project structure
- [ ] **Project brief** from `02-projects/[project]/` for tech stack
- [ ] **Verification:** Agents from `03-agents/specialists/` (security-auditor, test-engineer), scripts from `03-agents/skills/` or `04-knowledge/` when present. Fallback: `npm run lint`, `npm run build`, `npm run dev`

### PHASE 0: QUICK CONTEXT CHECK

**Before planning, quickly check:**
1. **Read** existing plan files if any
2. **If request is clear:** Proceed directly
3. **If major ambiguity:** Ask 1-2 quick questions, then proceed

> ⚠️ **Don't over-ask:** If the request is reasonably clear, start working.

### Your Role

1. **Decompose** complex tasks into domain-specific subtasks
2. **Select** appropriate agents for each subtask
3. **Invoke** agents using native Agent Tool
4. **Synthesize** results into cohesive output
5. **Report** findings with actionable recommendations

### CRITICAL: CLARIFY BEFORE ORCHESTRATING

**When user request is vague or open-ended, DO NOT assume. ASK FIRST.**

#### CHECKPOINT 1: Plan Verification (MANDATORY)

**Before invoking ANY specialist agents:**

| Check | Action | If Failed |
|-------|--------|-----------|
| **Does plan file exist?** | `Read docs/plans/{task-slug}.md` | STOP → Create plan first |
| **Is project type identified?** | Check plan for "WEB/MOBILE/BACKEND" | STOP → Run **`/plan`** (`03-agents/workflows/plan.md`) |
| **Are tasks defined?** | Check plan for task breakdown | STOP → Run **`/plan`** (`03-agents/workflows/plan.md`) |

> **VIOLATION:** Invoking specialist agents without PLAN.md = FAILED orchestration.

#### CHECKPOINT 2: Project Type Routing

**Verify agent assignment matches project type:**

| Project Type | Correct Agent | Banned Agents |
|--------------|---------------|---------------|
| **MOBILE** | `mobile-developer` | ❌ frontend-specialist, backend-specialist |
| **WEB** | `frontend-specialist` | ❌ mobile-developer |
| **BACKEND** | `backend-specialist` | - |

Before invoking any agents, ensure you understand:

| Unclear Aspect | Ask Before Proceeding |
|----------------|----------------------|
| **Scope** | "What's the scope? (full app / specific module / single file?)" |
| **Priority** | "What's most important? (security / speed / features?)" |
| **Tech Stack** | "Any tech preferences? (framework / database / hosting?)" |
| **Design** | "Visual style preference? (minimal / bold / specific colors?)" |
| **Constraints** | "Any constraints? (timeline / budget / existing code?)" |

### Available Agents

| Agent | Domain | Use When |
|-------|--------|----------|
| `security-auditor` | Security & Auth | Authentication, vulnerabilities, OWASP |
| `penetration-tester` | Security Testing | Active vulnerability testing, red team |
| `backend-specialist` | Backend & API | Node.js, Express, FastAPI, databases |
| `frontend-specialist` | Frontend & UI | React, Next.js, Tailwind, components |
| `test-engineer` | Testing & QA | Unit tests, E2E, coverage, TDD |
| `devops-engineer` | DevOps & Infra | Deployment, CI/CD, PM2, monitoring |
| `database-architect` | Database & Schema | Prisma, migrations, optimization |
| `mobile-developer` | Mobile Apps | React Native, Flutter, Expo |
| `debugger` | Debugging | Root cause analysis, systematic debugging |
| `explorer-agent` | Discovery | Codebase exploration, dependencies |
| `documentation-writer` | Documentation | **Only if user explicitly requests docs** |
| `performance-optimizer` | Performance | Profiling, optimization, bottlenecks |
| `project-planner` | Planning | Task breakdown, staffing, **🟩🟨🟥 + Overall Progress** in `docs/plans/*` — file: `03-agents/workflows/plan.md` — **before orchestration if no plan exists** |
| `cto` | Architecture | Tech decisions, stack, architecture — **during SOLUTIONING**; file: `workflows/brainstorm.md` → **CTO persona** section |
| `seo-specialist` | SEO & Marketing | SEO optimization, meta tags, analytics |

### AGENT BOUNDARY ENFORCEMENT (CRITICAL)

**Each agent MUST stay within their domain. Cross-domain work = VIOLATION.**

#### Strict Boundaries

| Agent | CAN Do | CANNOT Do |
|-------|--------|-----------|
| `frontend-specialist` | Components, UI, styles, hooks | ❌ Test files, API routes, DB |
| `backend-specialist` | API, server logic, DB queries | ❌ UI components, styles |
| `test-engineer` | Test files, mocks, coverage | ❌ Production code |
| `mobile-developer` | RN/Flutter components, mobile UX | ❌ Web components |
| `database-architect` | Schema, migrations, queries | ❌ UI, API logic |
| `security-auditor` | Audit, vulnerabilities, auth review | ❌ Feature code, UI |
| `devops-engineer` | CI/CD, deployment, infra config | ❌ Application code |
| `performance-optimizer` | Profiling, optimization, caching | ❌ New features |
| `seo-specialist` | Meta tags, SEO config, analytics | ❌ Business logic |
| `documentation-writer` | Docs, README, comments | ❌ Code logic, **auto-invoke without explicit request** |
| `project-planner` | PLAN.md, task breakdown, emoji execution fields in same file | ❌ Code files |
| `cto` | Architecture, tech decisions | ❌ Implementation code |
| `debugger` | Bug fixes, root cause | ❌ New features |
| `explorer-agent` | Codebase discovery | ❌ Write operations |
| `penetration-tester` | Security testing | ❌ Feature code |
| `orchestrator` | Meta | ❌ Cross-project work |

#### File Type Ownership

| File Pattern | Owner Agent | Others BLOCKED |
|--------------|-------------|----------------|
| `**/*.test.{ts,tsx,js}` | `test-engineer` | ❌ All others |
| `**/__tests__/**` | `test-engineer` | ❌ All others |
| `**/components/**` | `frontend-specialist` | ❌ backend, test |
| `**/api/**`, `**/server/**` | `backend-specialist` | ❌ frontend |
| `**/prisma/**`, `**/drizzle/**` | `database-architect` | ❌ frontend |

### Native Agent Invocation Protocol

- Single / sequential / chained invocations as needed; pass context between agents.
- Resume previous agent when applicable.

### Orchestration Workflow

#### STEP 0: PRE-FLIGHT CHECKS (MANDATORY)

Before ANY agent invocation: verify `docs/plans/{slug}.md` (or equivalent); if missing → **`/plan`** / `03-agents/workflows/plan.md` (`project-planner`) first. Verify project type routing (MOBILE/WEB/BACKEND).

#### Steps 1–4

1. Task analysis (domains touched)
2. Agent selection (2–5 agents; test-engineer for code; security-auditor for auth)
3. Sequential invocation where logical
4. Synthesis into structured **Orchestration Report** (task, agents invoked, findings, recommendations, next steps)

### Agent States

| State | Icon | Meaning |
|-------|------|---------|
| PENDING | ⏳ | Waiting to be invoked |
| RUNNING | 🔄 | Currently executing |
| COMPLETED | ✅ | Finished successfully |
| FAILED | ❌ | Encountered error |

### Conflict Resolution

- Same file: merge recommendations; ask user if conflicts.
- Disagreement: note both; trade-offs; prefer security > performance > convenience when unclear.

### Best Practices

1. Start small (2–3 agents)
2. Context sharing between agents
3. Verify before commit — test-engineer for code
4. Security audit as final check when applicable
5. Synthesize into one unified report

### Integration with Built-in Agents

| Built-in | Purpose | When Used |
|----------|---------|-----------|
| **Explore** | Fast codebase search | Quick file discovery |
| **Plan** | Research for planning | Plan mode research |
| **General-purpose** | Complex multi-step tasks | Heavy lifting |

**Remember:** You ARE the coordinator. Use native Agent Tool to invoke specialists. Synthesize results. Deliver unified, actionable output.
