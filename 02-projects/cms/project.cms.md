---
project: cms
status: active
path: ~/.gemini/antigravity/projects/cms
type: WEB
agents: [frontend-specialist, backend-specialist, database-architect, seo-specialist]
---

# CMS Monorepo

React + TypeScript CMS with component versioning, Firebase backend, multi-vertical (goldira, weightloss). Admin CMS, feature-based architecture, React Query.

## Goal
Comparison/affiliate content sites. Admin panel for content, shared components across verticals.

## Tech Stack
- **Frontend:** React 19.2, TypeScript, Vite, Tailwind v3.4, Framer Motion, React Hook Form, React Router v7, React Quill
- **State:** React State, Context, TanStack Query
- **Backend:** Firebase — Firestore, Cloud Functions, Auth, Hosting, Storage
- **Monorepo:** pnpm, Turbo
- **Shared:** @cms/shared, @vertical-configs/*
- **Testing:** Vitest, Playwright, Storybook, MSW
- **Monitoring:** Sentry, Firebase Analytics
- **Code:** ESLint, Biome, Husky, Commitlint, Knip

## How to run
```sh
pnpm install
# Copy apps/frontend/.env.example → apps/frontend/.env.local
pnpm dev
```
Dev server: port 5174 (goldira). `pnpm dev:weightloss` for weightloss.

## Workflow
1. Brainstorm feature or bug
2. Clarifying questions until understood
3. Discovery prompt for Cursor (file names, structure)
4. Break into phases, Cursor prompts per phase, status reports

## Status
Active.

## Decisions
- Multi-vertical architecture
- Shared workspace: @cms/shared

## Docs
See [[02-projects/cms/README|cms docs index]] — architecture, security, standards, remaining tasks (all in vault).

## Links
- Path: `~/.gemini/antigravity/projects/cms`
- Related: [[03-agents/content/gold-ira-seo-content-writer]]
