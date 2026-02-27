# Maestro — Deep Research Report

> **Date:** 2026-02-27  
> **Type:** Research, analysis, recommendations  
> **Goal:** In-depth study of the Maestro project as an agent infrastructure, identifying strengths, gaps, questions, and recommendations for optimal workflow

---

## 1. Executive Summary

**Maestro** is an Obsidian-based Second Brain that serves as the AI agent infrastructure for all development projects. The structure is well-established: agent-routing, specialist agents, structured workflows, and integration with Cursor via CLAUDE.md.  
The infrastructure is suitable as a base for any project — but there are gaps in practical implementation (project connectivity, Antigravity dependency) and steps are needed to make it more generic and practical.

---

## 2. What I Think About Maestro

### Notable Strengths

| Aspect | Assessment |
|--------|------------|
| **Hierarchical structure** | 00–07 clear, easy to navigate, fits PKM |
| **agent-routing** | Precise Trigger Matrix table — task routing to agents works well |
| **Agent quality** | frontend-specialist, orchestrator, project-planner — detailed and professional |
| **Separation of concerns** | Core / Specialists / Content / Workflows — proper separation |
| **Orchestration protocol** | 2-Phase, minimum 3 agents, user approval — prevents impulsiveness |
| **Agent Boundary Enforcement** | Each agent in its domain — reduces conflicts |
| **Plan Lifecycle** | Mandatory docs after execution, plan deletion — maintains cleanliness |
| **01-me** | Personal/business context — Xsheva, hadaryaCRM — enables tailored responses |

### Weaknesses

| Aspect | Problem |
|--------|---------|
| **Project connectivity** | 02-projects — each project has a folder. Source of truth for brief |
| **Enforcement** | 01-me, agent-routing, project brief — AI must read on its own; no technical rules that enforce |
| **Structure gaps** | 01-me/system missing (principles, routines); docs/plans outside 00–07 hierarchy |

---

## 3. Clarifying Questions

### 3.1 Work Environment

1. **Where do you actually work?**
   - Is Cursor open on the vault itself?
   - Or on a project folder (hadaryaCRM, cms) with symlink?

2. **Approved model:** Workspace = Vault (Maestro). Work on development projects when workspace is the vault.

### 3.2 02-projects

4. **What information is important in the project brief?**
   - Only: Goal, Tech Stack, Status?
   - Or also: architecture decisions, links to plans, link to relevant agents?

5. **How many active projects?**
   - hadaryaCRM, cms, proposal-generator, smart-volume-radar, website, source6681 — all active?
   - Does each need a brief?

### 3.3 Workflows

6. **create-plan vs project-planner:**
   - `create-plan` = plan with 🟩🟨🟥
   - `project-planner` = PLAN.md + task breakdown + agent assignment
   - Are the two complementary or overlapping? When to use which?

7. **docs/plans vs docs/plans:**
   - `plan-lifecycle` says: delete plan after execution
   - `project-planner` writes `./{task-slug}.md` in project root
   - `execute` says: `docs/plans/`
   - **Where are Plans really?** project root or docs/plans?

### 3.4 Gold IRA / Content

8. **Gold IRA Content Writer** — Still in use?
   - Niche-specific agent; if not relevant — can move to archive or remove from routing.

---

## 4. Unclear Matters

### 4.1 Connectivity Architecture

```
[User] → Cursor
            ↓
       workspace = ?
            ↓
   [Vault] or [Project folder]
            ↓
   CLAUDE.md loaded? 01-me? agent-routing?
            ↓
   Agent activated → project (code)
```

**Unclear:**
- When working on hadaryaCRM — is Cursor open on `~/.gemini/antigravity/projects/hadaryaCRM`?
- Does it have `maestro/` → symlink to vault?
- Or always work from the vault and open files at external path?

### 4.2 (Updated) Approved Model

- **No maestro.config.json** — removed. Source of truth: project brief in 02-projects
- **No .agent/ folder** — Vault (Maestro) replaced it. Agent infrastructure = the vault
- **Workspace = Vault** — work on development projects when workspace is the vault

### 4.4 Workflow Order

- `/plan` → project-planner? or create-plan?
- `/execute` → after `/plan`? What's the relation to orchestrate?
- Is `/orchestrate` = plan + execute + 3+ agents combined?

---

## 5. Topics for Refinement and Improvement

### 5.1 Maestro ↔ Project Connection (High Priority)

**Goal:** Every development project can use Maestro without creating manual symlinks.

**Recommendations:**

1. **Onboarding template for new project**
   - File: `05-templates/project-onboarding.md`
   - Steps: Create folder in 02-projects, project brief

2. **Document "how to connect a project"**
   - `docs/MAESTRO-ONBOARDING.md` — step-by-step instructions for connecting a new project

### 5.2 (Updated) No .agent/ — Vault Replaced It

**Status:** Maestro vault is the agent infrastructure. No `.agent/` folder.  
**Done:** Workflows updated — use `npm run lint`, `npm run build`, `npm run dev`.

### 5.3 01-me/system — Creation

**Problem:** PKM recommends; vault-verification plan noted — not created.

**Recommendations:**

1. **Create 01-me/system/**
   - `README.md` — explanation
   - `principles.md` — Inbox first, Agent per task, Verify before completion
   - `routines.md` — Weekly: process inbox, update 07-logs; Before project: read brief

2. **Update CLAUDE.md**
   - Add: "Before complex tasks — read 01-me/system/principles if relevant"

### 5.4 Plan Consistency

**Problem:** project-planner → `./{task-slug}.md` (project root); execute → `docs/plans/`; plan-lifecycle → `docs/plans/`.

**Recommendation:**
- **Single decision:** Plans always in `docs/plans/` (in vault or in project)
- Update project-planner: `docs/plans/{task-slug}.md` or `./docs/plans/{task-slug}.md` (relative to project)
- Clear docs: vault plans = general planning; project plans = code planning

### 5.5 create-plan vs project-planner

**Recommendation:**
- **project-planner** = complex planning, task breakdown, agent assignment, PLAN.md
- **create-plan** = light planning, 🟩🟨🟥, no agent assignment
- In agent-routing: clarify when each — e.g. "create-plan" for "simple task with clear steps"

### 5.6 Frontmatter in Workflows

**Status:** Previous reports noted missing `name` — now in document.md, execute.md, orchestrate.md etc. — `name` exists.  
**Check:** Ensure all 17 workflows include `name` in frontmatter.

---

## 6. Optimal Workflow — Maestro as Infrastructure for Every Project

### 6.1 Recommended Model

```
┌─────────────────────────────────────────────────────────────┐
│  MAESTRO VAULT = WORKSPACE                                  │
│  • CLAUDE.md, 01-me, 03-agents                              │
│  • 02-projects = folder per project + project brief         │
│  • 06-outputs = deliverables                               │
│  • No .agent/ — vault = agent infrastructure                │
└─────────────────────────────────────────────────────────────┘
         │
         │  Before task: Read project brief
         │  Route: agent-routing.md
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PROJECT (code — external path or within vault)              │
│  • docs/plans/ — temporary plans (in vault or in project)    │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Recommended Workflow

| Step | Action |
|------|--------|
| **1. New project** | Create folder `02-projects/[name]/` + `project.[name].md` (from template) |
| **2. Before task** | Read project brief. Read agent-routing. Identify trigger → agent |
| **3. Simple task** | Single agent (e.g. frontend-specialist) |
| **4. Complex task** | orchestrate → project-planner → user approval → specialists (parallel) |
| **5. After execution** | document workflow, delete plan, log in 07-logs |

### 6.3 Recommended Cursor Setup

**Option A — Vault as Workspace (simple)**
- Open Cursor on Maestro vault
- Projects as paths — `~/.../hadaryaCRM` etc.
- CLAUDE.md loaded automatically
- **Downside:** Not "inside" the project; must mention paths

**Option B — Multi-Root**
- Cursor with multiple roots: Maestro + hadaryaCRM
- CLAUDE.md from vault + code from project
- **Advantage:** Full context on both sides

**Option C — Project = Workspace + Symlink**
- Open Cursor on hadaryaCRM
- Inside: `maestro/` → symlink to vault
- Add to .cursor/rules or workspace settings: "Load 01-me, 03-agents from maestro/"
- **Advantage:** Work "inside" the project; Maestro available

**Recommendation:** Try **Option C** — most natural for a developer working daily in the project.

### 6.4 New Project Onboarding — Checklist

1. [ ] Create folder `02-projects/[project]/`
2. [ ] Create `project.[name].md` (from template) — Goal, Tech Stack, Status, path
3. [ ] Workspace = Vault — Cursor open on vault
4. [ ] Test: "Build X" → agent-routing → project-planner → OK?

---

## 7. Additional Aspects

### 7.1 Skills vs Agents

- **Agents** = persona + behavior (frontend-specialist, orchestrator)
- **Skills** = external capabilities (clean-code, frontend-design) — mentioned in frontmatter
- **Location:** Cursor skills or links within the vault

### 7.2 Language

- Agents and workflows — **English** (suits Cursor/Claude)
- 01-me, 02-projects, logs — Hebrew suitable (personal/business context)
- **Consistency:** Examples in orchestrate (Turkish, Vietnamese) — replace with English

### 7.3 Archive and Drift

- Plans deleted after execution — good
- **09-archive/** — doesn't exist; PKM recommended
- **Drift:** New agents — is agent-routing updated? Automated sync check (script) would help

### 7.4 Observability

- No logs yet of "which agent was activated, when, on what"
- **Idea:** 07-logs — entry for each significant session (project, agent, task, outcome)

### 7.5 Testing the System

- **Recommended test:** Simulation marathon
  - "Build a dashboard with charts" → should: project-planner → approval → frontend + backend + test
  - "Fix bug in login" → debugger
  - "Do code review" → review workflow
- If something doesn't work — fix routing or docs

---

## 8. Summary of Recommended Actions (by Priority)

| # | Action | Priority |
|---|--------|----------|
| 1 | Create 01-me/system/ (principles, routines) | High |
| 2 | Document "how to connect a project to Maestro" (onboarding) | High |
| 3 | Plan location consistency (docs/plans) | Medium |
| 6 | Check frontmatter `name` in 17 workflows | Low |
| 7 | Replace non-English examples | Low |
| 8 | 09-archive (optional) | Low |

---

## 9. Conclusion

Maestro is a **professional and well-designed** agent infrastructure. Its strengths: clear routing, quality agents, structured orchestration protocol. For it to serve **every** development project:

1. **02-projects** — folder per project, full brief, learn when to read
3. **Define onboarding** — new project = clear checklist
4. **Workspace = Vault** — approved and documented

The questions in section 3 will help refine implementation. After answers — a precise implementation plan can be outlined.

---

*Created: 2026-02-27 | Sources: CLAUDE.md, agent-routing, workflows, specialists, outputs, plans, PKM analysis, rules audit*
