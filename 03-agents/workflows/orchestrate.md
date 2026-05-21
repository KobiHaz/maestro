---
name: orchestrate
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# Multi-Agent Orchestration

You are now in **ORCHESTRATION MODE**. Your task: coordinate specialized agents to solve this complex problem.

**Maestro routing:** This workflow is the vault’s structured multi-agent path alongside [[agent-routing]] — orchestrate and invoke specialists from `03-agents/`; do not substitute their domain work. **Orchestrator persona** is embedded in `agent-routing.md` (there is no `core/orchestrator.md`).

## Place in the supply cycle

- **Stage:** **Coordination** (often parallel) — not a substitute for specification, task planning, or line-by-line `/execute`.
- **Before:** plan in `docs/plans/{slug}.md` or create it in phase 1 of this protocol (**`workflows/plan.md`** / `project-planner` only + sometimes `explorer-agent`).
- **After:** synthesis → continue per plan (usually **`/execute`** or another coordination round). Minimum **3 distinct agents** — otherwise it is not orchestration.
- **Staffing:** every agent from [[agent-routing]] and per plan staffing.

---

## Coordination Mode: Subagents vs Agent Teams

Two modes available. Choose based on whether agents need to talk to each other.

| Mode | When | How |
|------|------|-----|
| **Subagents** (default) | Agents work independently, results synthesized by orchestrator | Agent tool — agents report back sequentially |
| **Agent Teams** | Agents need to share findings, debate, or coordinate in real time | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — teammates message each other directly |

### Use Agent Teams when:
- **Competing hypotheses** — multiple agents investigating different root causes, actively trying to disprove each other
- **Comprehensive audits** — security-auditor, explorer-agent, and performance-optimizer running truly in parallel and sharing discoveries as they find them
- **Cross-domain features** — frontend, backend, and test-engineer need to coordinate on shared interfaces in real time
- **Research with debate** — 3+ perspectives that need to challenge each other before consensus

### How to spawn an Agent Team (example prompt to the lead)
```
Create an agent team for this task. Spawn three teammates:
- security-auditor: audit the auth module for vulnerabilities
- explorer-agent: map the full codebase architecture and dependencies
- backend-specialist: review the API layer for security and performance

Have them share findings with each other as they discover issues and reach a consensus report.
```

**Available user-scope teammate definitions** (`~/.claude/agents/`):
`security-auditor` · `frontend-specialist` · `backend-specialist` · `explorer-agent` · `test-engineer`

**Feature flag:** already enabled vault-wide via `~/.claude/settings.json` (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

**Token cost:** Agent Teams use significantly more tokens — each teammate is a full Claude session. Reserve for scenarios where inter-agent communication genuinely changes the outcome.

---

## Task to Orchestrate
$ARGUMENTS

---

## Workspace Model

**Workspace = Maestro vault.** Projects live in `02-projects/` (brief) and code lives in project folders.

**No `.agent/` folder** — The vault replaced it. Agents, tools, and skills live in:
- **03-agents/** — specialists (security-auditor, test-engineer, etc.), core, workflows, skills
- **04-knowledge/** — research, guidelines, scripts

Verification uses agents from `03-agents/specialists/` and scripts from `03-agents/skills/` or `04-knowledge/` when present.

---

## 🔴 CRITICAL: Minimum Agent Requirement

> ⚠️ **ORCHESTRATION = MINIMUM 3 DIFFERENT AGENTS**
> 
> If you use fewer than 3 agents, you are NOT orchestrating - you're just delegating.
> 
> **Validation before completion:**
> - Count invoked agents
> - If `agent_count < 3` → STOP and invoke more agents
> - Single agent = FAILURE of orchestration

### Agent Selection Matrix

| Task Type | REQUIRED Agents (minimum) |
|-----------|---------------------------|
| **Web App** | frontend-specialist, backend-specialist, test-engineer |
| **API** | backend-specialist, security-auditor, test-engineer |
| **UI/Design** | frontend-specialist, seo-specialist, performance-optimizer |
| **Database** | database-architect, backend-specialist, security-auditor |
| **Full Stack** | `workflows/plan.md` (project-planner), frontend-specialist, backend-specialist, devops-engineer |
| **Debug** | debugger, explorer-agent, test-engineer |
| **Security** | security-auditor, penetration-tester, devops-engineer |

---

## Pre-Flight: Mode Check

| Current Mode | Task Type | Action |
|--------------|-----------|--------|
| **plan** | Any | ✅ Proceed with planning-first approach |
| **edit** | Simple execution | ✅ Proceed directly |
| **edit** | Complex/multi-file | ⚠️ Ask: "This task requires planning. Switch to plan mode?" |
| **ask** | Any | ⚠️ Ask: "Ready to orchestrate. Switch to edit or plan mode?" |

---

## 🔴 STRICT 2-PHASE ORCHESTRATION

### PHASE 1: PLANNING (Sequential - NO parallel agents)

| Step | Agent | Action |
|------|-------|--------|
| 1 | `project-planner` (`03-agents/workflows/plan.md`) | Create `docs/plans/{task-slug}.md` (same convention as [[workflows/plan]]) |
| 2 | (optional) `explorer-agent` | Codebase discovery if needed |

> 🔴 **NO OTHER AGENTS during planning!** Only **`workflows/plan.md`** (project-planner) and explorer-agent.

### ⏸️ CHECKPOINT: User Approval

```
After `docs/plans/{task-slug}.md` is complete (see [[workflows/plan]]), ASK:

"Plan created: docs/plans/<slug>.md

Approve plan? (Y/N)
- Y: Implementation starts
- N: I will revise the plan"
```

> 🔴 **DO NOT proceed to Phase 2 without explicit user approval!**

### PHASE 2: IMPLEMENTATION (Parallel agents after approval)

| Parallel Group | Agents |
|----------------|--------|
| Foundation | `database-architect`, `security-auditor` |
| Core | `backend-specialist`, `frontend-specialist` |
| Polish | `test-engineer`, `devops-engineer` |

> ✅ After user approval, invoke multiple agents in PARALLEL.

## Available Agents (17 total)

| Agent | Domain | Use When |
|-------|--------|----------|
| `project-planner` | Planning | Task breakdown, `docs/plans/*.md` — file: `03-agents/workflows/plan.md` |
| `explorer-agent` | Discovery | Codebase mapping |
| `frontend-specialist` | UI/UX | React, Vue, CSS, HTML |
| `backend-specialist` | Server | API, Node.js, Python |
| `database-architect` | Data | SQL, NoSQL, Schema |
| `security-auditor` | Security | Vulnerabilities, Auth |
| `penetration-tester` | Security | Active testing |
| `test-engineer` | Testing | Unit, E2E, Coverage |
| `devops-engineer` | Ops | CI/CD, Docker, Deploy |
| `mobile-developer` | Mobile | React Native, Flutter |
| `performance-optimizer` | Speed | Lighthouse, Profiling |
| `seo-specialist` | SEO | Meta, Schema, Rankings |
| `documentation-writer` | Docs | README, API docs |
| `debugger` | Debug | Error analysis |
| `orchestrator` | Meta | Coordination |

---

## Orchestration Protocol

### Step 1: Analyze Task Domains
Identify ALL domains this task touches:
```
□ Security     → security-auditor, penetration-tester
□ Backend/API  → backend-specialist
□ Frontend/UI  → frontend-specialist
□ Database     → database-architect
□ Testing      → test-engineer
□ DevOps       → devops-engineer
□ Mobile       → mobile-developer
□ Performance  → performance-optimizer
□ SEO          → seo-specialist
□ Planning     → `workflows/plan.md` (project-planner)
```

### Step 2: Phase Detection

| If Plan Exists | Action |
|----------------|--------|
| NO `docs/plans/{slug}.md` | → Go to PHASE 1 (planning only) |
| YES `docs/plans/{slug}.md` + user approved | → Go to PHASE 2 (implementation) |

### Step 3: Execute Based on Phase

**PHASE 1 (Planning):**
```
Use **`/plan`** / `03-agents/workflows/plan.md` (project-planner) to create the plan file
→ STOP after plan is created
→ ASK user for approval
```

**PHASE 2 (Implementation - after approval):**
```
Invoke agents in PARALLEL:
Use the frontend-specialist agent to [task]
Use the backend-specialist agent to [task]
Use the test-engineer agent to [task]
```

**🔴 CRITICAL: Context Passing (MANDATORY)**

When invoking ANY subagent, you MUST include:

1. **Original User Request:** Full text of what user asked
2. **Decisions Made:** All user answers to Socratic questions
3. **Previous Agent Work:** Summary of what previous agents did
4. **Current Plan State:** If `docs/plans/` has a plan, include it

**Example with FULL context:**
```
Use **`/plan`** / `03-agents/workflows/plan.md` (project-planner) to create the plan file:

**CONTEXT:**
- User Request: "Öğrenciler için sosyal platform, mock data ile"
- Decisions: Tech=Vue 3, Layout=Grid Widget, Auth=Mock, Design=Genç Dinamik
- Previous Work: Orchestrator asked 6 questions, user chose all options
- Current Plan: docs/plans/dashboard-analytics.md exists with initial structure

**TASK:** Create detailed `docs/plans/{task-slug}.md` per [[workflows/plan]] based on ABOVE decisions. Do NOT infer from folder name.
```

> ⚠️ **VIOLATION:** Invoking subagent without full context = subagent will make wrong assumptions!


### Step 4: Verification (MANDATORY)
The LAST agent must run verification. Use agents from `03-agents/specialists/` and scripts from vault when present:

1. **Security** — Invoke `security-auditor` agent, or run:
   ```bash
   python 03-agents/skills/vulnerability-scanner/scripts/security_scan.py .   # if present
   ```

2. **Lint & Type** — Invoke `test-engineer` agent, or run:
   ```bash
   python 03-agents/skills/lint-and-validate/scripts/lint_runner.py .       # if present
   npm run lint && npx tsc --noEmit   # or project-standard fallback
   ```

3. **Build** — `npm run build`

### Step 5: Synthesize Results
Combine all agent outputs into unified report.

---

## Output Format

```markdown
## 🎼 Orchestration Report

### Task
[Original task summary]

### Mode
[Current Claude Code mode: plan/edit/ask]

### Agents Invoked (MINIMUM 3)
| # | Agent | Focus Area | Status |
|---|-------|------------|--------|
| 1 | project-planner (`workflows/plan.md`) | Task breakdown | ✅ |
| 2 | frontend-specialist | UI implementation | ✅ |
| 3 | test-engineer | Verification scripts | ✅ |

### Verification Executed
- [x] security-auditor / security_scan.py → Pass/Fail
- [x] lint_runner.py or npm run lint → Pass/Fail
- [x] build → Pass/Fail

### Key Findings
1. **[Agent 1]**: Finding
2. **[Agent 2]**: Finding
3. **[Agent 3]**: Finding

### Deliverables
- [ ] `docs/plans/{slug}.md` created
- [ ] Code implemented
- [ ] Tests passing
- [ ] security-auditor verification
- [ ] lint / typecheck verification
- [ ] build verification

### Summary
[One paragraph synthesis of all agent work]
```

---

## 🔴 EXIT GATE

Before completing orchestration, verify:

1. ✅ **Agent Count:** `invoked_agents >= 3`
2. ✅ **Verification:** security-auditor (or security_scan.py), test-engineer (or lint_runner.py), build executed
3. ✅ **Report Generated:** Orchestration Report with all agents listed

> **If any check fails → DO NOT mark orchestration complete. Invoke more agents or run scripts from 03-agents/skills/ or 04-knowledge/.**

---

**Begin orchestration now. Select 3+ agents, execute sequentially, run verification (agents + scripts from vault), synthesize results.**
