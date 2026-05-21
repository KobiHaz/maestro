---
project: crm
status: active
path: ~/.gemini/antigravity/projects/hadaryaCRM
type: WEB
agents: [frontend-specialist, backend-specialist, test-engineer, security-auditor]
---

# CRM

Custom CRM for clients. Primary active project.

## Goal
Build and maintain a custom CRM with UX tailored to client workflows.

## Tech Stack
- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query v5

## How to run
```sh
bun install && bun run dev
```

## Status
Active development.

## Decisions
- **13.3.2026** — Gemini UX Audit: Sprints 1–3 complete (scroll fixes, sticky columns, tab badges, RTL).
- **24.2.2026** — Modular permissions: replaced global user_roles with user_module_roles + profiles.super_admin.
- **2026-04-29** — Knowledge migrated from Obsidian to .claude/ in project repo.

## Docs
See [CRM docs index](README.md) — UI-UX plan, security audit, Cursor MCP, plans.

## Links
- Path: `~/.gemini/antigravity/projects/hadaryaCRM`
- Knowledge layer: project `.claude/CLAUDE.md` (source of truth for Claude)
