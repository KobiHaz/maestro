# CLAUDE — Second Brain Instructions

Main instruction file (read automatically when working with this vault).

## Workspace Model

- **Workspace = Maestro vault** — Cursor opens on the vault; project code is accessed from project paths
- **02-projects** — One folder per project; each has a project brief (source of truth for stack, status, decisions)
- **No maestro.config.json** — Removed. Use project brief in 02-projects.
- **No .agent/ folder** — The vault replaced it. Agents, tools, skills in `03-agents/`, `04-knowledge/`. Scripts when present in `03-agents/skills/`. Fallback: `npm run lint`, `npm run build`, `npm run dev`

## Folder Structure

| Folder | Purpose |
|--------|---------|
| **00-inbox** | Entry point — ideas, links, quick notes |
| **01-me** | Identity — who you are, style, tools, preferences |
| **02-projects** | Projects — summary, status, decisions |
| **03-agents** | Agents, workflows, vault skills — index: `03-agents/skills/README.md` |
| **04-knowledge** | Knowledge base — research, competitor analysis, insights |
| **05-templates** | Templates — posts, summaries, emails |
| **06-outputs** | Final outputs — files with date in filename |
| **07-logs** | Logs — automatic documentation of actions |

## Basic Instructions

1. **Inbox first** — Capture new items in 00-inbox before processing
2. **Projects** — Each project gets its own note in 02-projects with status and decisions
3. **Outputs** — Name final deliverables with date (e.g. `2026-02-26-Report.md`)
4. **Logs** — Document significant actions and decisions in 07-logs

## Agent Protocol

- **New idea / feature / change** — Start with specification: `03-agents/workflows/brainstorm.md` (**`/brainstorm`** + CTO persona in that file). **PRD** (`/prd`) and **`/plan`** — `03-agents/workflows/plan.md` (PRD section + task planning). Then implement or run **`/execute`** per plan.
- **Before every task** — Read 01-me (identity, business context)
- **Before every task** — Read `03-agents/agent-routing.md` and invoke the matching agent proactively (do not wait for user to tag)
- **Before writing content** — Read 01-me/01-me-writing (tone, style)
- **Before project work** — Read the project brief from 02-projects

## Coding Standards

When writing or reviewing code: load `04-knowledge/standards/base-coding-standards.md` + project standards from 04-knowledge/standards/.

**Quick reference:** No `any`; normalize data at fetch boundary; hooks `use`+PascalCase; TanStack Query for server state.

## Knowledge & Outputs

- **Before new research** — Check if information already exists in 04-knowledge
- **Save outputs** — In 06-outputs with date in filename
- **Templates** — Use 05-templates when format exists

## Comprehensive Project Audit

When user requests **מחקר מעמיק**, **סקירה מקיפה**, **comprehensive audit**, or **activation of all agents** for a project:
1. Invoke `project-deep-audit` workflow (03-agents/workflows/project-deep-audit.md)
2. **Always load:** 02-projects brief, 04-knowledge/reference/*, 04-knowledge/standards/*
3. **Use:** explorer-agent + relevant specialists + scripts from 03-agents/skills/
4. **Output** → 06-outputs/YYYY-MM-DD-<project>-audit-report.md

## Plan Execution & Documentation

- **Two layers** — Ongoing project tasks: `02-projects/<project>/plans-and-tasks.md` (single source of truth). Ephemeral step-by-step execution: `docs/plans/*.md` while implementing; sync back, then remove per `04-knowledge/standards/maestro-project-doc-lifecycle.md`
- **After plan execution** — Update or create documentation for the changes (`03-agents/workflows/document.md`)
- **After plan execution** — Delete the plan file from `docs/plans/` (no persistence needed)
- **Logs** — Document significant executions in `07-logs/`

Customize this file with your own workflow rules.
